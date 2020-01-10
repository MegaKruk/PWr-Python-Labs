import random as rnd
import matplotlib.pyplot as plt
#import imageio
import pylab
import networkx as nx
import numpy as np


def qvoter(g0, p=0.5, q=4, epsilon=0):
    number_of_nodes = len(g0.nodes())
    labels = {}
    m = [0] * 1000
    for j in range(100):
        for h in range(number_of_nodes):
            labels[h] = 1
        for i in range(1000):
            spinson = rnd.randint(0, number_of_nodes - 1)
            # zdecydowanie z prawd p czy spinson będzie niezależny
            # mniejsze od p to niezależny, większe od p zależny
            r = rnd.random()
            if r < p:  # niezależny
                r2 = rnd.random()
                if r2 < 0.5:
                    labels[spinson] = (-1) * labels[spinson]
            else:
                neighbor = list(g0.neighbors(spinson))
                if len(neighbor) < q:
                    chosen = neighbor
                else:
                    chosen = np.random.choice(neighbor, q, replace=False)
                list_of_decision = []
                for k in range(len(chosen)):
                    list_of_decision.append(labels[chosen[k]])
                if min(list_of_decision) == max(list_of_decision):
                    labels[spinson] = min(list_of_decision)
                else:
                    if rnd.random() < epsilon:
                        labels[spinson] = (-1) * labels[spinson]
            m[i] = m[i] + ((sum(labels.values())) / len(labels.values()))
    return m


if __name__ == "__main__":

    GraphWS1 = nx.watts_strogatz_graph(100, 4, 0.01)
    GraphWS2 = nx.watts_strogatz_graph(100, 4, 0.2)
    GraphBA = nx.barabasi_albert_graph(100, 4)
    GraphC = nx.complete_graph(100)

    m1  = qvoter(GraphWS1,0.5,3)
    m2  = qvoter(GraphWS2,0.5,3)
    m3 = qvoter(GraphBA,0.5,3)
    m4 = qvoter(GraphC,0.5,3)

    plt.figure()
    plt.plot(m1, label='WS(100,4,0.01)') 
    plt.plot(m2, label='WS(100,4,0.2)')    
    plt.plot(m3, label='BA(100,4)')
    plt.plot(m4, label='complete graph')
    plt.legend()
    plt.title('Average magnetization in time for q = 3 and p = 0.5')
    plt.xlabel('time')
    plt.ylabel('magnetization')
    pylab.savefig('av_mag_q3_p05.png')
    plt.show()

    m1  = qvoter(GraphWS1,0.5,4)
    m2  = qvoter(GraphWS2,0.5,4)
    m3 = qvoter(GraphBA,0.5,4)
    m4 = qvoter(GraphC,0.5,4)

    plt.figure()
    plt.plot(m1, label='WS(100,4,0.01)')    
    plt.plot(m2, label='WS(100,4,0.2)')
    plt.plot(m3, label='BA(100,4)')
    plt.plot(m4, label='complete graph')
    plt.legend()
    plt.title('Average magnetization in time for q = 4 and p = 0.5')
    plt.xlabel('time')
    plt.ylabel('magnetization')
    pylab.savefig('av_mag_q4_p05.png')
    plt.show()

    m1 = qvoter(GraphWS1, 0.25, 3)
    m2 = qvoter(GraphWS2, 0.25, 3)
    m3 = qvoter(GraphBA, 0.25, 3)
    m4 = qvoter(GraphC, 0.25, 3)

    plt.figure()
    plt.plot(m1, label='WS(100,4,0.01)')
    plt.plot(m2, label='WS(100,4,0.2)')
    plt.plot(m3, label='BA(100,4)')    
    plt.plot(m4, label='complete graph')
    plt.legend()
    plt.title('Average magnetization in time for q = 3 and p = 0.25')
    plt.xlabel('time')
    plt.ylabel('magnetization')
    pylab.savefig('av_mag_q3_p025.png')
    plt.show()

    m1 = qvoter(GraphWS1, 0.25, 4)
    m2 = qvoter(GraphWS2, 0.25, 4)
    m3 = qvoter(GraphBA, 0.25, 4)
    m4 = qvoter(GraphC, 0.25, 4)

    plt.figure()
    plt.plot(m1, label='WS(100,4,0.01)')    
    plt.plot(m2, label='WS(100,4,0.2)')
    plt.plot(m3, label='BA(100,4)')
    plt.plot(m4, label='complete graph')
    plt.legend()
    plt.title('Average magnetization in time for q = 4 and p = 0.25')
    plt.xlabel('time')
    plt.ylabel('magnetization')
    pylab.savefig('av_mag_q4_p025.png')
    plt.show()


prob_vec = np.linspace(0.0, 0.5, 25)
m_final_BA = []
m_final_WS1 = []
m_final_WS2 = []
m_final_C = []
i=0
for prob in prob_vec:
    m1 = qvoter(GraphWS1, prob, 3)
    m2 = qvoter(GraphWS2, prob, 3)
    m3 = qvoter(GraphBA, prob,3)    
    m4 = qvoter(GraphC, prob, 3)
    m_final_WS1.append(m1[-1] / 100)
    m_final_WS2.append(m2[-1] / 100)    
    m_final_BA.append(m3[-1]/100)
    m_final_C.append(m4[-1] / 100)
    i=i+1
    print(i)

m_final_BAq4 = []
m_final_WS1q4 = []
m_final_WS2q4 = []
m_final_Cq4 = []
for prob in prob_vec:
    m1 = qvoter(GraphWS1, prob, 4)
    m2 = qvoter(GraphWS2, prob, 4)    
    m3 = qvoter(GraphBA, prob, 4)
    m4 = qvoter(GraphC, prob, 4)
    m_final_WS1q4.append(m1[-1] / 100)
    m_final_WS2q4.append(m2[-1] / 100)    
    m_final_BAq4.append(m3[-1]/100)
    m_final_Cq4.append(m4[-1] / 100)
    i = i + 1
    print(i)

plt.figure()
plt.plot(prob_vec, m_final_WS1, label='WS(100,4,0.2)')
plt.plot(prob_vec, m_final_WS2, label='WS(100,4,0.1)')
plt.plot(prob_vec, m_final_BA, label='BA(100,4)')
plt.plot(prob_vec, m_final_C, label='complete graph')
plt.legend()
plt.title('Average final magnetization for q = 3')
plt.xlabel('probability')
plt.ylabel('magnetization')
pylab.savefig('av_final_mag_q3.png')
plt.show()

plt.figure()
plt.plot(prob_vec, m_final_BAq4, label='BA(100,4)')
plt.plot(prob_vec, m_final_WS1q4, label='WS(100,4,0.2)')
plt.plot(prob_vec, m_final_WS2q4, label='WS(100,4,0.01)')
plt.plot(prob_vec, m_final_Cq4, label='complete graph')
plt.legend()
plt.title('Average final magnetization for q = 4')
plt.xlabel('probability')
plt.ylabel('magnetization')
pylab.savefig('av_final_mag_q4.png')
plt.show()

plt.figure()
plt.plot(prob_vec,m_final_WS1,label='q=3')
plt.plot(prob_vec, m_final_WS1q4,label='q=4')
plt.legend()
plt.title('Average final magnetization for WS(100,4,0.01)')
plt.xlabel('probability')
plt.ylabel('magnetization')
pylab.savefig('av_final_mag_WS1.png')
plt.show()
