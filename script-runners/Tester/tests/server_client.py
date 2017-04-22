from ..base.test import Test, grade
import copy
import socket, struct
import time

class ServerClient(Test):
    description = "Server Client"
    order = 3
    enabled = True
    test_order = ['test_client_server_get_ip', 'test_client_server_accept_offer',
                  'test_client_server_lease', 'test_client_server_time']
    save_judge_mode = False

    def before(self):
        client_count = 5
        self.kill_clients()
        self.new_map()
        client_dict = {0:'c', 1:'c', 2:'c', 3:'j', 4:'j'}
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

    @grade(25)
    def test_client_server_get_ip(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        self.clients[4].write_io('add pool 192.160.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('get ip')
        time.sleep(2*self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_client_server_get_ip')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(0), message='Output for node 0 did not match', end=False, grade=5)
            self.assert_true(self.check_send_frames(0), message='send frames node 0 did not match', end=False, grade=10)
            self.assert_true(self.check_output(1), message='Output for node 1 did not match', end=False, grade=5)
            self.assert_true(self.check_send_frames(1), message='send frames node 1 did not match', end=False, grade=5)

    @grade(25)
    def test_client_server_accept_offer(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        self.clients[4].write_io('add pool 192.160.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('get ip')
        time.sleep(2*self.sleep_time)
        self.clients[0].write_io('accept offer: 192.168.1.8')
        time.sleep(2*self.sleep_time)
        self.clients[2].write_io('accept offer: 192.160.1.8')
        time.sleep(2*self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_client_server_accept_offer')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(1), message='Output for node 0 did not match', end=False, grade=5)
            self.assert_true(self.check_send_frames(1), message='send frames node 0 did not match', end=False, grade=10)
            self.assert_true(self.check_output(2), message='Output for node 2 did not match', end=False, grade=5)
            self.assert_true(self.check_send_frames(2), message='send frames node 2 did not match', end=False, grade=5)

    @grade(25)
    def test_client_server_lease(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        self.clients[4].write_io('add pool 192.160.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('get ip')
        time.sleep(2*self.sleep_time)
        self.clients[2].write_io('accept offer: 192.160.1.8')
        time.sleep(2*self.sleep_time)
        self.clients[2].write_io('extend lease 192.160.1.8')
        time.sleep(2*self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_client_server_lease')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(2), message='Output for node 2 did not match', end=False, grade=10)
            self.assert_true(self.check_send_frames(2), message='send frames node 2 did not match', end=False, grade=15)

    @grade(25)
    def test_client_server_time(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        self.clients[4].write_io('add pool 192.160.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[2].write_io('get ip')
        time.sleep(2 * self.sleep_time)
        self.clients[2].write_io('accept offer: 192.160.1.8')
        time.sleep(2 * self.sleep_time)
        self.clients[2].write_io('extend lease 192.160.1.8')
        time.sleep(2 * self.sleep_time)
        self.clients[4].write_io('add time 8')
        # time.sleep(self.sleep_time)
        self.clients[4].write_io('add time 15')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_client_server_time')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(2), message='Output for node 2 did not match', end=False, grade=10)
            self.assert_true(self.check_send_frames(2), message='send frames node 2 did not match', end=False, grade=15)

# ===================================================================================================================================================== #
