class SimulationService:
    def __init__(self, strategy, start_date, end_date, interval):
        """
        Initializes the Simulation Service with the given parameters.

        :param strategy: An instance of the trading strategy class you wish to test.
        :param start_date: The start date for the simulation in 'YYYY-MM-DD' format.
        :param end_date: The end date for the simulation in 'YYYY-MM-DD' format.
        :param interval: The time interval for each step of the simulation (e.g., '5min', '1h', '1d').
        """
        self.strategy = strategy
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.current_date = (
            start_date  # Keeps track of the current date in the simulation.
        )
        # You might want to add more attributes for tracking performance metrics, orders, etc.

    def fetch_data(self, date):
        """
        Fetches or computes the data for the given date.

        :param date: The date for which to fetch the data.
        :return: The market data for the specified date.
        """
        # Implement the logic to fetch or compute the required data for the given date.
        # This could involve querying a database, reading from a file, etc.
        pass

    def execute_step(self):
        """
        Executes a single step of the simulation, applying the trading strategy to the current data.
        """
        data = self.fetch_data(self.current_date)
        decision = self.strategy.decide(
            data
        )  # Assume your strategy class has a 'decide' method.
        # Implement the logic to execute the trading decision and update the simulation state.
        self.update_simulation_state(decision)

    def update_simulation_state(self, decision):
        """
        Updates the state of the simulation based on the decision made by the strategy.

        :param decision: The decision made by the trading strategy.
        """
        # Implement the logic to update your simulation's state, such as open positions,
        # account balance, etc., based on the strategy's decision.
        pass

    def run(self):
        """
        Runs the simulation over the specified date range and interval.
        """
        while self.current_date <= self.end_date:
            self.execute_step()
            # Implement the logic to advance self.current_date by self.interval.
            # This might involve date and time manipulation using a library like 'datetime'.

    # Add additional methods as needed, such as for performance evaluation, logging, etc.
