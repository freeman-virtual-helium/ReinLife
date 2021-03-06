
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random
from collections import deque
from.utils import BasicBrain

# gamma = 0.99
# learning_rate = 1e-3
# batch_size = 64
# capacity = 10000


class D3QNAgent(BasicBrain):
    """ Dueling Double Deep Q Network

    Parameters:
    -----------
    input_dim : int, default 153
        The input dimension

    output_dim : int, default 8
        The output dimension

    exploration : int, default 1000
        The number of epochs to explore the environment before learning

    soft_update_freq : int, default 200
        The frequency at which to align the target and eval nets

    train_freq : int, default 20
        The frequency at which to train the agent

    learning_rate : float, default 1e-3
        Learning rate

    batch_size : int
        The number of training samples to work through before the model's internal parameters are updated.

    gamma : float, default 0.98
        Discount factor. How far out should rewards in the future influence the policy?

    capacity : int, default 10_000
        Capacity of replay buffer

    load_model : str, default False
        Path to an existing model

    training : bool, default True,
        Whether to continue training or not
    """
    def __init__(self, input_dim=153, output_dim=8, exploration=1000, soft_update_freq=200, train_freq=20,
                 learning_rate=1e-3, gamma=0.99, batch_size=64, capacity=10000, load_model=False, training=True):
        super().__init__(input_dim, output_dim, "D3QN")

        self.target_net = dueling_ddqn(input_dim, output_dim)
        self.eval_net = dueling_ddqn(input_dim, output_dim)
        self.eval_net.load_state_dict(self.target_net.state_dict())
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=learning_rate)
        self.buffer = replay_buffer(capacity)
        self.loss_fn = nn.MSELoss()
        self.exploration = exploration
        self.soft_update_freq = soft_update_freq
        self.train_freq = train_freq
        self.n_epi = 0
        self.epsilon = 0.9
        self.epsilon_min = 0.05
        self.decay = 0.99
        self.batch_size = batch_size
        self.gamma = gamma

        self.training = training
        if not self.training:
            self.epsilon = 0

        if load_model:
            self.eval_net.load_state_dict(torch.load(load_model))
            self.eval_net.eval()

    def get_action(self, state, n_epi):

        if self.training:
            # Update epsilon once
            if n_epi > self.n_epi:
                if self.epsilon > self.epsilon_min:
                    self.epsilon = self.epsilon * self.decay
                self.n_epi = n_epi

        action = self.eval_net.act(torch.FloatTensor(np.expand_dims(state, 0)), self.epsilon)
        return action

    def memorize(self, obs, action, reward, next_obs, done):
        self.buffer.store(obs, action, reward, next_obs, done)

    def train(self):
        observation, action, reward, next_observation, done = self.buffer.sample(self.batch_size)

        observation = torch.FloatTensor(observation)
        action = torch.LongTensor(action)
        reward = torch.FloatTensor(reward)
        next_observation = torch.FloatTensor(next_observation)
        done = torch.FloatTensor(done)

        q_values = self.eval_net.forward(observation)
        next_q_values = self.target_net.forward(next_observation)
        next_q_value = next_q_values.max(1)[0].detach()
        q_value = q_values.gather(1, action.unsqueeze(1)).squeeze(1)
        expected_q_value = reward + self.gamma * (1 - done) * next_q_value

        loss = self.loss_fn(q_value, expected_q_value)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def learn(self, age, dead, action, state, reward, state_prime, done, n_epi):
        self.memorize(state, action, reward, state_prime, done)

        if n_epi > self.exploration:
            if age % self.train_freq == 0 or dead:
                self.train()

            if n_epi % self.soft_update_freq == 0:
                self.target_net.load_state_dict(self.eval_net.state_dict())


class replay_buffer(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = deque(maxlen=self.capacity)

    def store(self, observation, action, reward, next_observation, done):
        observation = np.expand_dims(observation, 0)
        next_observation = np.expand_dims(next_observation, 0)
        self.memory.append([observation, action, reward, next_observation, done])

    def sample(self, batch_size):
        batch = random.sample(self.memory, batch_size)
        observation, action, reward, next_observation, done = zip(* batch)
        return np.concatenate(observation, 0), action, reward, np.concatenate(next_observation, 0), done

    def __len__(self):
        return len(self.memory)


class dueling_ddqn(nn.Module):
    def __init__(self, observation_dim, action_dim):
        super(dueling_ddqn, self).__init__()
        self.observation_dim = observation_dim
        self.action_dim = action_dim
        self.fc = nn.Linear(self.observation_dim, 128)

        self.adv_fc1 = nn.Linear(128, 128)
        self.adv_fc2 = nn.Linear(128, self.action_dim)

        self.value_fc1 = nn.Linear(128, 128)
        self.value_fc2 = nn.Linear(128, 1)

    def forward(self, observation):
        feature = self.fc(observation)
        advantage = self.adv_fc2(F.relu(self.adv_fc1(F.relu(feature))))
        value = self.value_fc2(F.relu(self.value_fc1(F.relu(feature))))
        return advantage + value - advantage.mean()

    def act(self, observation, epsilon):
        if random.random() > epsilon:
            q_value = self.forward(observation)
            action = q_value.max(1)[1].data[0].item()
        else:
            action = random.choice(list(range(self.action_dim)))
        return action




