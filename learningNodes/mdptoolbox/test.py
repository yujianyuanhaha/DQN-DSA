import mdptoolbox

P, R = mdptoolbox.example.forest()
pi = mdptoolbox.mdp.PolicyIteration(P, R, 0.9)
pi.run()
expected = (26.244000000000014, 29.484000000000016, 33.484000000000016)
all(expected[k] - pi.V[k] < 1e-12 for k in range(len(expected)))
print pi.policy