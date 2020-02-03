from unittest import TestCase
import testUtility
import Dominion


class TestAction_card(TestCase):

    def setUp(self):
        # Data setup
        self.player_names = testUtility.get_player_names()
        self.nV = testUtility.get_num_victory_cards(self.player_names)
        self.nC = testUtility.get_num_curse_cards(self.player_names)
        self.box = testUtility.get_box(self.nV)
        self.supply_order = testUtility.get_supply_order()
        self.supply = testUtility.get_supply(self.box, self.player_names, self.nV, self.nC)
        self.trash = []

    def test_init(self):
        # Intialize test
        self.setUp()
        name = "test card"
        cost = 0
        actions = 0
        cards = 0
        buys = 0
        coins = 0

        # Make Card object
        testCard = Dominion.Action_card(name, cost, actions, cards, buys, coins)

        # Verify the class variables have the expected values
        self.assertEqual(testCard.name, name)
        self.assertEqual(testCard.cost, cost)
        self.assertEqual(testCard.actions, actions)
        self.assertEqual(testCard.cards, cards)
        self.assertEqual(testCard.buys, buys)
        self.assertEqual(testCard.coins, coins)
        self.assertEqual(testCard.category, "action")
        self.assertEqual(testCard.buypower, 0)
        self.assertEqual(testCard.vpoints, 0)

    def test_use(self):
        # Intialize test
        self.setUp()

        name = "Test Card"
        cost = 3
        actions = 3
        cards = 3
        buys = 3
        coins = 3

        # Set up the cards for the players hand
        testCard1 = Dominion.Action_card(name, cost, actions, cards, buys, coins)
        testCard2 = Dominion.Action_card(name, cost, actions, cards, buys, coins)

        # Set up the Player
        testPlayer = Dominion.Player("Daniel")

        # Add the cards to the hand
        testPlayer.hand.append(testCard1)
        testPlayer.hand.append(testCard2)

        targetList = testPlayer.hand.copy()

        # Confirm the starting conditions
        self.assertListEqual(testPlayer.hand, targetList)
        self.assertListEqual(testPlayer.played, [])

        # Remove a card and check the lists
        testCard1.use(testPlayer, self.trash)
        targetList.remove(testCard1)
        self.assertListEqual(testPlayer.hand, targetList)
        self.assertListEqual(testPlayer.played, [testCard1])

        # Remove another card and check the lists
        testCard2.use(testPlayer, self.trash)
        targetList.remove(testCard2)
        self.assertListEqual(testPlayer.hand, targetList)
        self.assertListEqual(testPlayer.played, [testCard1, testCard2])

    def test_augment(self):
        # Intialize test
        self.setUp()

        name = "Test Card"
        cost = 3
        actions = 3
        cards = 3
        buys = 3
        coins = 3

        # Set up the card
        testCard = Dominion.Action_card(name, cost, actions, cards, buys, coins)

        # Set up the Player
        testPlayer = Dominion.Player("Daniel")

        # Initialize the players values
        testPlayer.actions = 0
        testPlayer.buys = 0
        testPlayer.purse = 0

        # Activate the function
        testCard.augment(testPlayer)

        # Verify the results
        self.assertEqual(testPlayer.actions, 3)
        self.assertEqual(testPlayer.buys, 3)
        self.assertEqual(testPlayer.purse, 3)
        self.assertEqual(len(testPlayer.hand), 8)


class TestPlayer(TestCase):

    def setUp(self):
        # Data setup
        self.player_names = testUtility.get_player_names()
        self.nV = testUtility.get_num_victory_cards(self.player_names)
        self.nC = testUtility.get_num_curse_cards(self.player_names)
        self.box = testUtility.get_box(self.nV)
        self.supply_order = testUtility.get_supply_order()
        self.supply = testUtility.get_supply(self.box, self.player_names, self.nV, self.nC)
        self.trash = []

    def test_draw(self):
        # Intialize test
        self.setUp()

        # Set up the Player
        testPlayer = Dominion.Player("Daniel")

        # Verify Starting conditions
        self.assertEqual(len(testPlayer.deck), 5)
        self.assertEqual(len(testPlayer.discard), 0)
        self.assertEqual(len(testPlayer.hand), 5)

        # Activate draw and test the conditions
        testPlayer.draw()

        self.assertEqual(len(testPlayer.deck), 4)
        self.assertEqual(len(testPlayer.discard), 0)
        self.assertEqual(len(testPlayer.hand), 6)

        # Draw to the discard 4 times and check conditions
        testPlayer.draw(testPlayer.discard)
        testPlayer.draw(testPlayer.discard)
        testPlayer.draw(testPlayer.discard)
        testPlayer.draw(testPlayer.discard)

        self.assertEqual(len(testPlayer.deck), 0)
        self.assertEqual(len(testPlayer.discard), 4)
        self.assertEqual(len(testPlayer.hand), 6)

        # Draw one more time and test conditions
        testPlayer.draw()

        self.assertEqual(len(testPlayer.deck), 3)
        self.assertEqual(len(testPlayer.discard), 0)
        self.assertEqual(len(testPlayer.hand), 7)

    def test_action_balance(self):
        # Intialize test
        self.setUp()

        actionCard = Dominion.Festival()

        # Set up the Player
        testPlayer = Dominion.Player("Daniel")

        # Run the function
        self.assertEqual(testPlayer.action_balance(), 0)

        # Add an action card with actions to the stack and verify
        testPlayer.deck.append(actionCard)
        self.assertEqual(testPlayer.action_balance(), (70*1/11))

        # Add an action card with actions to the stack and verify
        testPlayer.deck.append(actionCard)
        self.assertEqual(testPlayer.action_balance(), (70*2/12))


    def test_cardsummary(self):
        # Intialize test
        self.setUp()

        # Set up the Player
        testPlayer = Dominion.Player("Daniel")

        # Run the function
        summary = testPlayer.cardsummary()

        # Build expected results
        expectedResults = {"Copper":7, "Estate":3, "VICTORY POINTS":3}

        # Verify the results
        self.assertDictEqual(summary, expectedResults)

    def test_calcpoints(self):
        # Intialize test
        self.setUp()

        gardenCard = Dominion.Gardens()

        # Set up the Player
        testPlayer = Dominion.Player("Daniel")

        # Run the function
        self.assertEqual(testPlayer.calcpoints(), 3)

        # Add an action card with actions to the stack and verify
        testPlayer.deck.append(gardenCard)
        self.assertEqual(testPlayer.calcpoints(), 4)

        # Add an action card with actions to the stack and verify
        testPlayer.deck.append(gardenCard)
        self.assertEqual(testPlayer.calcpoints(), 5)
