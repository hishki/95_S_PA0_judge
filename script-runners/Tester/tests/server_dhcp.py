from ..base.test import Test, grade
import copy
import socket, struct
import time

class ServerSimple(Test):
    description = "Server Simple"
    order = 2
    enabled = True
    test_order = ['test_server_get_ip', 'test_server_accept_offer', 'test_server_add_time']
    save_judge_mode = False

    def before(self):
        client_count = 13
        self.kill_clients()
        self.new_map()
        client_dict = {0:'j', 1:'c'}
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

    @grade(35)
    def test_server_get_ip(self):
        self.clients[1].write_io('add pool 192.168.1.1/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_server_get_ip')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(1), message='Output for node 1 did not match', end=False, grade=20)
            self.assert_true(self.check_send_frames(1), message='send frames node 1 did not match', end=False, grade=15)

    @grade(35)
    def test_server_accept_offer(self):
        self.clients[1].write_io('add pool 192.168.1.1/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('accept offer: 192.168.1.0')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_server_accept_offer')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(1), message='Output for node 1 did not match', end=False, grade=20)
            self.assert_true(self.check_send_frames(1), message='send frames node 1 did not match', end=False, grade=15)

    @grade(30)
    def test_server_add_time(self):
        self.clients[1].write_io('add pool 192.168.1.1/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('accept offer: 192.168.1.0')
        time.sleep(self.sleep_time)
        self.clients[1].write_io('add time 10')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_server_add_time')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(1), message='Output for node 1 did not match', end=False, grade=15)
            self.assert_true(self.check_send_frames(1), message='send frames node 1 did not match', end=False, grade=15)
# ===================================================================================================================================================== #
