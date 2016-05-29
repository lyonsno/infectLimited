This package requires python3 to run.  Activate a virtualenv and 'pip3 install -r requirements.text'.  It uses matplotlib 1.4.3 instead of 1.5.1 because of a bug when using pip requirments.txt with matplotlib 1.5.1, that would require an extra file to be created by the user in the virtualenv directery. Matplotlib 1.4.3 is completely sufficient.

After the environment is set up, tests can be run as follows:

to run unit tests, run the command python3 -m pytest ./test/unitTests/

to evaluate the efficacy of the solution, run the command python3 -m pytest --tb=short ./test/evaluateSolutionQuality.  
This test will run the algorithm multiple times on a persistent set of twenty randomly generated graphs designed to model connections between learners and coaches.  Some of the graphs in test_infect_limted.py contain subsets of disconnected graphs.  Graphs in test_infect_limited.py are all completely connected.  Graphs in test_infect_limited_quick.py are smaller and fewer test iterations are run, so solutions are less accurate but the tests run more quickly.

to visualize the performance of the algorithm, run the command python3 -m pytest ./test/visualize/
These images will display smaller graphs for clarity.  Red nodes are the epicenter of infection, and green nodes are infected.  Black nodes are not infected.