import pytest
from user import User

def test_has_coach():
	userA = User()
	userB = User()

	assert not userA.has_coach(userB)
	
def test_can_add_coach():
	userA = User()
	userB = User()

	userA.add_coach(userB)

	assert userA.has_coach(userB)

def test_has_coachee():
	userA = User()
	userB = User()

	assert not userA.has_coachee(userB)

def test_add_coachee():
	userA = User()
	userB = User()

	userA.add_coachee(userB)

	assert userA.has_coachee(userB)

def test_infect():
	userA = User()

	userA.infect()

	assert userA.infected

def test_infect_neighbor_coachees():
	userA = User()
	userB = User()
	userC = User()

	userA.add_coachee(userB)
	userA.add_coachee(userC)

	userA.infect_coachees()

	assert userB.infected and userC.infected

def test_infect_neighbor_coaches():
	userA = User()
	userB = User()
	userC = User()

	userA.add_coach(userB)
	userA.add_coach(userC)

	userA.infect_coaches()

	assert userB.infected and userC.infected

def test_infect_neighbors():
	userA = User()
	userB = User()
	userC = User()

	userA.add_coach(userB)
	userA.add_coachee(userC)

	userA.infect()

	assert userB.infected and userC.infected

def test_infect_network():
	userA = User()
	userB = User()
	userC = User()
	userD = User()
	userE = User()

	userA.add_coach(userB)
	userA.add_coachee(userC)
	userC.add_coach(userD)
	userB.add_coachee(userE)
	userA.infect()

	assert userA.infected and userB.infected and userC.infected and userD.infected and userE.infected

def test_infect_disconnected():
	userA = User()
	userB = User()

	userA.infect()

	assert not userB.infected

def test_cycle_network():
	userA = User()
	userB = User()
	userC = User()

	userA.add_coach(userB)
	userB.add_coach(userC)
	userC.add_coach(userA)

	userA.infect()

	assert userA.infected and userB.infected and userC.infected