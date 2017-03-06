from ..base.test import Test, grade
import copy
import socket, struct
import time

class ClientSimple(Test):
    description = "Client Simple"
    order = 1
    enabled = True
    test_order = ['test_client_get_ip', 'test_client_accept_offer', 'test_client_release']
    save_judge_mode = False

    def before(self):
        client_count = 13
        self.kill_clients()
        self.new_map()
        client_dict = {0:'c', 1:'j'}
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
    def test_client_get_ip(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_client_get_ip')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(0), message='Output for node 0 did not match', end=False, grade=20)
            self.assert_true(self.check_send_frames(0), message='send frames node 0 did not match', end=False, grade=15)

    @grade(35)
    def test_client_accept_offer(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('accept offer: 192.168.1.8')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_client_accept_offer')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(0), message='Output for node 0 did not match', end=False, grade=20)
            self.assert_true(self.check_send_frames(0), message='send frames node 0 did not match', end=False, grade=15)

    @grade(30)
    def test_client_release(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('accept offer: 192.168.1.8')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('release 192.168.1.8')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_client_release')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(0), message='Output for node 0 did not match', end=False, grade=15)
            self.assert_true(self.check_send_frames(0), message='send frames node 0 did not match', end=False, grade=15)
# ===================================================================================================================================================== #
