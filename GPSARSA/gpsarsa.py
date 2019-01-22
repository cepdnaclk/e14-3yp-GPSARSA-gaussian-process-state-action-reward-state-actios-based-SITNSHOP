import numpy as np
from GPSARSA.Kernal.RBF import RBF


class GPSARSA():

    def __init__(self, r, threshold, variance,  start_state, ini_reward, constant_white_noise = 0.01):
        self.variance = variance
        self.threshold = threshold
        self.r = r
        self.D = np.reshape(np.array([start_state]), (1, len(start_state)))
        self.D_len = 1
        self.no_visisted_states = 1
        self.constant_white_noise = constant_white_noise


        self.previous_state = None
        self.curr_state = start_state

        #approximation_parameters
        self.weight = np.array([[1]])
        self.k_cap = np.array([])
        self.weight_sol = np.array([1])
        self.delta_k_cap = np.array([1])
        self.delta_k_tt = np.array([1])

        #parameters for the computation of mean and variance
        self.reward = np.reshape(np.array([ini_reward]), newshape=(1,1))
        self.alpha_cap = np.reshape(np.array([0]), (1,1))
        self.C_cap = np.reshape(np.array([0]), (1,1))
        self.K_cap_inverse = np.array([1/RBF(start_state, start_state)])
        self.H_cap = None
        self.Q_cap  = None


    def compute_k_cap(self, new_state):
        self.k_cap = np.array([RBF(a=self.D[i],b =  new_state) for i in range(len(self.D))])

    def compute_k_cap_r(self, new_state):

        return np.array([RBF(a=self.D[i],b =  new_state) for i in range(len(self.D))])

    def comput_k_cap_for_mean_var(self, new_state, add_state = True):

        if add_state == False:
            return np.array([RBF(a=self.D[i],b =  new_state) for i in range(len(self.D))])
        else:
            D = np.append(self.D, np.reshape(new_state, (1, len(new_state))), axis=0)
            return np.array([RBF(a=D[i],b =  new_state) for i in range(len(D))])

    def sparsification_test(self, new_state):


        return RBF(new_state, new_state) - np.dot(self.k_cap, self.weight_sol)

    def iterate(self, new_state, reward, with_update = True):

        self.compute_k_cap(new_state)
        self.weight_sol = np.reshape( np.dot(self.K_cap_inverse, self.k_cap), (self.D_len, 1))

        error =  self.sparsification_test(new_state)


        if error < self.threshold:

            if self.no_visisted_states == 1:

                self.previous_state = self.curr_state
                self.curr_state = new_state

                self.weight = np.append(self.weight, self.weight_sol.T, axis=0)
                h = np.reshape(self.weight[-1] - self.r*self.weight_sol.T, ( self.D_len, 1))
                self.H_cap = np.reshape(np.array([h]), (1,1))
                #no update in K_cap
                self.Q_cap  = np.reshape(1/(np.dot(self.H_cap, np.dot(self.K_cap_inverse, self.H_cap.T)) + self.constant_white_noise), (1,1))


                self.alpha_cap = np.dot(self.H_cap.T, np.dot(self.Q_cap, self.reward))
                self.C_cap = np.dot(self.H_cap.T, np.dot(self.Q_cap, self.H_cap))

                self.no_visisted_states += 1
                self.reward = np.append(self.reward, np.array([[reward]]))

            else:

                self.delta_k_cap = self.compute_k_cap_r(self.previous_state) - self.r*self.k_cap

                h = np.reshape(self.weight[-1] - self.r*self.weight_sol.T, ( self.D_len, 1))
                g  = np.reshape(np.dot(np.dot(self.Q_cap, self.H_cap), self.delta_k_cap), (self.no_visisted_states-1, 1))
                c =  np.dot(self.H_cap.T, g) - h
                s = self.constant_white_noise - np.dot(c.T, self.delta_k_cap.T)


                alpha_cap = self.alpha_cap + (c/s)*(np.dot(self.delta_k_cap, self.alpha_cap) - self.reward[-1])
                C_cap = self.C_cap + (1/s)*np.dot(c, c.T)

                k_caq_for_mv = self.comput_k_cap_for_mean_var(new_state, add_state=False)

                mean = np.dot(k_caq_for_mv.T, alpha_cap)
                variance = RBF(new_state, new_state) - np.dot(k_caq_for_mv.T, np.dot(C_cap, k_caq_for_mv))



                if with_update == True:
                #UPDATE PROCESS FOR THE NEXT STATE
                    self.Q_cap = (1/s)*np.block(
                        [[s*self.Q_cap + np.dot(g, g.T), -g],
                         [-g.T, 1]
                        ]
                    )

                    self.H_cap = np.append(self.H_cap, h.T, axis=0)
                    #K_cap_inverse remains constant
                    self.weight = np.append(self.weight, self.weight_sol.T, axis=0)

                    self.C_cap = C_cap
                    self.alpha_cap = alpha_cap

                    self.no_visisted_states += 1
                    self.reward = np.append(self.reward, np.array([[reward]]))
                    self.previous_state = self.curr_state
                    self.curr_state = new_state

                return (mean, variance)

        else:


            if self.no_visisted_states == 1:

                self.previous_state = self.curr_state
                self.curr_state = new_state

                self.H_cap = np.reshape(np.array([1, self.r]), (1,2))
                self.K_cap_inverse = (1/error)*np.block(
                    [[error*self.K_cap_inverse + np.dot(self.weight_sol, self.weight_sol.T), -self.weight_sol],
                     [-self.weight_sol.T, 1]
                    ]
                )

                self.Q_cap  = np.reshape(1/(np.dot(self.H_cap, np.dot(self.K_cap_inverse, self.H_cap.T)) + self.constant_white_noise), (1,1))

                self.weight = np.block(
                    [[self.weight, np.zeros((self.no_visisted_states, 1))],
                     [np.zeros((1, self.D_len)), 1]
                    ]
                )
                self.D = np.append(self.D, np.reshape(new_state, (1, len(new_state))), axis=0)
                self.D_len += 1


                self.alpha_cap = np.dot(self.H_cap.T, np.dot(self.Q_cap, self.reward))
                self.C_cap = np.dot(self.H_cap.T, np.dot(self.Q_cap, self.H_cap))

                self.no_visisted_states += 1
                self.reward = np.append(self.reward, np.array([[reward]]))

            else:

                self.delta_k_cap = self.compute_k_cap_r(self.previous_state) - self.r*self.k_cap
                self.delta_k_tt = np.dot(self.weight[-1].T, ( self.delta_k_cap - self.r*self.k_cap)) + self.r*self.r*RBF(new_state, new_state)

                s_cap = self.constant_white_noise + self.delta_k_tt - np.dot(self.delta_k_cap.T , np.dot(self.C_cap, self.delta_k_cap))
                g  = np.reshape(np.dot(np.dot(self.Q_cap, self.H_cap), self.delta_k_cap.T), (self.no_visisted_states-1, 1))
                c_cap = np.reshape(np.dot(self.H_cap.T, g) - np.reshape(self.weight[-1], (self.D_len, 1)), (self.D_len, 1 ))


                alpha_cap = np.append(
                    self.alpha_cap + (c_cap/s_cap)*(np.dot(self.delta_k_cap, self.alpha_cap) - self.reward[-1]),
                    np.reshape((self.r/s_cap)*(np.dot(self.delta_k_cap.T, self.weight[-1]) - self.reward[-1]), (1,1)), axis=0
                )

                C_cap = np.block(
                    [[self.C_cap + (1/s_cap)*np.dot(c_cap, c_cap.T), (self.r/s_cap)*c_cap],
                     [(self.r/s_cap)*c_cap.T, (self.r*self.r/s_cap)]
                    ]
                )


                k_caq_for_mv = self.comput_k_cap_for_mean_var(new_state, add_state=True)

                mean = np.dot(k_caq_for_mv.T, alpha_cap)
                variance = RBF(new_state, new_state) - np.dot(k_caq_for_mv.T, np.dot(C_cap, k_caq_for_mv))


                if with_update == True:
                #UPDATE PROCESS FOR THE NEXT STATE

                    self.previous_state = self.curr_state
                    self.curr_state = new_state


                    self.H_cap = np.block(
                        [[self.H_cap, np.zeros((self.no_visisted_states-1, 1))],
                         [self.weight[-1], -self.r]
                        ]
                    )

                    self.weight = np.block(
                        [[self.weight, np.zeros((self.no_visisted_states, 1))],
                         [np.zeros((1, self.D_len)), 1]
                        ]
                    )

                    self.K_cap_inverse = (1/error)*np.block(
                        [[error*self.K_cap_inverse + np.dot(self.weight_sol, self.weight_sol.T), -self.weight_sol],
                         [-self.weight_sol.T, 1]
                        ]
                    )

                    self.Q_cap = (1/s_cap)*np.block(
                        [[s_cap*self.Q_cap + np.dot(g, g.T), -g],
                         [-g.T, 1]
                        ]
                    )

                    self.alpha_cap = alpha_cap
                    self.C_cap = C_cap
                    self.D = np.append(self.D, np.reshape(new_state, (1, len(new_state))), axis=0)
                    self.D_len += 1
                    self.no_visisted_states += 1
                    self.reward = np.append(self.reward, np.array([[reward]]))

                return (mean, variance)

        #print("K_cap_inverse")
        #print(self.K_cap_inverse)
        #print("D")
        #print(self.D)
        #print("Weight")
        #print(self.weight)
        #print("H_cap")
        #print(self.H_cap)
        #print("C_cap")
        #print(self.C_cap)
        #print("alpha_cap")
        #print(self.alpha_cap)


'''
G = GPSARSA(0.2,5e-04,1,[1,1], 3)
G.iterate([1,1], 3)
G.iterate([2,3], 3)
G.iterate([3,3], 4)

G.iterate([10,20], 3, with_update=False)
G.iterate([2,2], 3, with_update=False)
G.iterate([1,1], 3, with_update=False)
G.iterate([50,40], 3, with_update=False)
print(G.D)
'''
