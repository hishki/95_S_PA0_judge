from ..base.test import Test, grade
import copy
import socket, struct
import time

class AllIn(Test):
    description = "All In"
    order = 4
    enabled = True
    test_order = ['test_all_in_extend', 'test_all_in_time']
    save_judge_mode = False

    def before(self):
        client_count = 5
        self.kill_clients()
        self.new_map()
        client_dict = {1:'c', 2:'c', 3:'c', 4:'c'}
        # client_dict = {0: 'j', 1: 'j', 2: 'j', 3: 'j'}
        self.start_clients(client_dict=client_dict)

        for client in self.clients.itervalues():
            client.wait_for_start()
        time.sleep(self.sleep_time)

    def after(self):
        self.kill_clients()
        self.free_map()

    def save_judge(self, path):
        self.client_manager.save_judge_all(path)

    def load_judge(self, path):
        self.client_manager.load_judge_all(path)
    # ===================================================================================================================================================== #

    @grade(50)
    def test_all_in_extend(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        self.clients[4].write_io('add pool 192.160.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('get ip')
        time.sleep(2*self.sleep_time)
        self.clients[2].write_io('accept offer: 192.168.1.8')
        time.sleep(2*self.sleep_time)
        self.clients[2].write_io('extend lease 192.168.1.8')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_all_in_extend')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(1), message='Output for node 1 did not match', end=False, grade=15)
            self.assert_true(self.check_send_frames(1), message='send frames node 1 did not match', end=False, grade=15)
            self.assert_true(self.check_output(2), message='Output for node 2 did not match', end=False, grade=10)
            self.assert_true(self.check_send_frames(2), message='send frames node 2 did not match', end=False, grade=10)

    @grade(50)
    def test_all_in_time(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        self.clients[4].write_io('add pool 192.160.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('get ip')
        time.sleep(2*self.sleep_time)
        self.clients[2].write_io('accept offer: 192.168.1.8')
        time.sleep(2*self.sleep_time)
        self.clients[2].write_io('extend lease 192.168.1.8')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('add time 8')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('add time 15')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_all_in_time')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(2), message='Output for node 2 did not match', end=False, grade=10)
            self.assert_true(self.check_send_frames(2), message='send frames node 2 did not match', end=False, grade=10)
            self.assert_true(self.check_output(1), message='Output for node 1 did not match', end=False, grade=15)
            self.assert_true(self.check_send_frames(1), message='send frames node 1 did not match', end=False, grade=15)

    # ===================================================================================================================================================== #
