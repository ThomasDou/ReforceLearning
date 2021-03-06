# coding=utf-8

import gym
from MyImprovedDQN import *
import os

env_name = 'CartPole-v0'
model_name = "./model/cartpole_improved_dqn.h5"
train_graph_name = "./graph/cartpole_improved_train_dqn.png"
test_graph_name = "./graph/cartpole_improved_test_dqn.png"

def train(graph_name, max_iter=20000, max_epsisodes=2000):
    env = gym.make(env_name)
    env = env.unwrapped
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    agent = DQNAgent(state_size, action_size, batch_size=64, train_start=100, C=100)


    if os.path.exists(model_name):
        agent.model.load_weights(model_name)

    scores, losses = [], []


    for epoch in range(max_epsisodes):
        score = 0
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        if np.mean(scores[-5:]) > 10000:
            break
        while score <= max_iter:
            if agent.render:
                agent.render()
            action = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])

            score += 1

            agent.add_memory(state, action, reward, done, next_state)
            agent.train_model()
            state = next_state

            if done or score >= max_iter:
                break
        if len(agent.losses_list) > 0:
            loss = np.array(agent.losses_list)
            print("(episode: {}; score: {}; memory length: {}; loss-mean: {})"
                      .format(epoch, score, len(agent.memory), loss.mean()))
            scores.append(score)
            losses.append(loss.mean())

        if epoch % 50 == 0:
            agent.model.save_weights(model_name)

    print('(reward mean: {}; reward std: {})'.format(np.array(scores).mean(), np.array(scores).std()))
    draw_plot(scores, losses, filename=graph_name)


def test(graph_name, max_iter=20000, max_epsisodes=500):
    env = gym.make(env_name)
    env = env.unwrapped
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    agent = DQNAgent(state_size, action_size, batch_size=64, train_start=100, epsilon=0.0001, render=False)

    if os.path.exists(model_name):
        agent.model.load_weights(model_name)

    scores = []

    for epoch in range(max_epsisodes):
        score = 0
        state = env.reset()
        state = np.reshape(state, [1, state_size])

        while score <= max_iter:
            if agent.render:
                env.render()
            action = agent.choose_action(state)
            next_state, reward, done, info = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            score += 1

            state = next_state

            if done or score >= max_iter:
                print("(episode: {}; score: {};)"
                      .format(epoch, score))
                scores.append(score)
                break

    print('(reward mean: {}; reward std: {})'.format(np.array(scores).mean(), np.array(scores).std()))
    draw_score_plot(scores, filename=graph_name)

if __name__ == '__main__':
    train(train_graph_name)
    test(test_graph_name)
