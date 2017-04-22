from ..base.test import Test, grade
import copy
import socket, struct
import time

class Others(Test):
    description = "Others"
    order = 5
    enabled = True
    test_order = ['test_others_print', 'test_others_release',
                  'test_others_accept_offer']
    save_judge_mode = False

    def before(self):
        client_count = 5
        self.kill_clients()
        self.new_map()
        client_dict = {0:'c', 1:'c'}
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

    @grade(80)
    def test_others_print(self):
        self.clients[1].write_io('add pool 192.168.1.10/30')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('accept offer: 192.168.1.8')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('get ip')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('accept offer: 192.168.1.9')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('release 192.168.1.8')
        time.sleep(self.sleep_time)
        self.clients[0].write_io('print ip')
        self.clients[1].write_io('print pool')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_others_print')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(0), message='Output for node 0 did not match', end=False, grade=20)
            self.assert_true(self.check_send_frames(0), message='send frames node 0 did not match', end=False, grade=20)
            self.assert_true(self.check_output(1), message='Output for node 1 did not match', end=False, grade=20)
            self.assert_true(self.check_send_frames(1), message='send frames node 1 did not match', end=False, grade=20)

    @grade(10)
    def test_others_release(self):
        self.clients[0].write_io('release 192.168.1.8')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_others_release')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(0), message='Output for node 0 did not match', end=False, grade=5)
            self.assert_true(self.check_send_frames(0), message='send frames node 0 did not match', end=False, grade=5)

    @grade(10)
    def test_others_accept_offer(self):
        self.clients[0].write_io('accept offer: 192.160.1.8')
        time.sleep(self.sleep_time)

        self.client_manager.get_clients_ready_to_judge('log/test_others_accept_offer')
        if not self.save_judge_mode:
            self.assert_true(self.check_output(0), message='Output for node 2 did not match', end=False, grade=5)
            self.assert_true(self.check_send_frames(0), message='send frames node 2 did not match', end=False, grade=5)

# ===================================================================================================================================================== #
