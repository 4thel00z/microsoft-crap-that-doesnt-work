
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: chat_client_sample.py
DESCRIPTION:
    These samples demonstrate create a chat client, get a chat thread client,
    create a chat thread, get a chat thread by id, list chat threads, delete
    a chat thread by id.
    You need to use azure.communication.configuration module to get user access
    token and user identity before run this sample

USAGE:
    python chat_client_sample.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_COMMUNICATION_SERVICE_ENDPOINT - Communication Service endpoint url
    2) TOKEN - the user access token, from token_response.token
    3) USER_ID - the user id, from token_response.identity
"""


import os


class ChatClientSamples(object):
    from azure.communication.identity import CommunicationIdentityClient
    connection_string = os.environ.get("AZURE_COMMUNICATION_SERVICE_CONNECTION_STRING", None)
    if not connection_string:
        raise ValueError("Set AZURE_COMMUNICATION_SERVICE_CONNECTION_STRING env before run this sample.")

    identity_client = CommunicationIdentityClient.from_connection_string(connection_string)
    user = identity_client.create_user()
    tokenresponse = identity_client.get_token(user, scopes=["chat"])
    token = tokenresponse.token

    endpoint = os.environ.get("AZURE_COMMUNICATION_SERVICE_ENDPOINT", None)
    if not endpoint:
        raise ValueError("Set AZURE_COMMUNICATION_SERVICE_ENDPOINT env before run this sample.")

    _thread_id = None

    def create_chat_client(self):
        # [START create_chat_client]
        from azure.communication.chat import ChatClient
        from azure.communication.identity._shared.user_credential import CommunicationTokenCredential
        from azure.communication.chat._shared.user_token_refresh_options import CommunicationTokenRefreshOptions
        refresh_options = CommunicationTokenRefreshOptions(self.token)
        chat_client = ChatClient(self.endpoint, CommunicationTokenCredential(refresh_options))
        # [END create_chat_client]

    def create_thread(self):
        # [START create_thread]
        from datetime import datetime

        from azure.communication.identity import CommunicationUserIdentifier
        from azure.communication.identity._shared.user_credential import CommunicationTokenCredential
        from azure.communication.chat._shared.user_token_refresh_options import CommunicationTokenRefreshOptions

        from azure.communication.chat import(
            ChatClient,
            ChatThreadParticipant
        )

        refresh_options = CommunicationTokenRefreshOptions(self.token)
        chat_client = ChatClient(self.endpoint, CommunicationTokenCredential(refresh_options))

        topic = "test topic"
        participants = [ChatThreadParticipant(
            user=self.user,
            display_name='name',
            share_history_time=datetime.utcnow()
        )]

        # creates a new chat_thread everytime
        create_chat_thread_result = chat_client.create_chat_thread(topic, thread_participants=participants)

        # creates a new chat_thread if not exists
        repeatability_request_id = 'b66d6031-fdcc-41df-8306-e524c9f226b8' # unique identifier
        create_chat_thread_result_w_repeatability_id = chat_client.create_chat_thread(
            topic,
            thread_participants=participants,
            repeatability_request_id=repeatability_request_id
        )
        # [END create_thread]

        self._thread_id = create_chat_thread_result.chat_thread.id
        print("thread created, id: " + self._thread_id)

    def get_chat_thread_client(self):
        # [START get_chat_thread_client]
        from azure.communication.chat import ChatClient
        from azure.communication.identity._shared.user_credential import CommunicationTokenCredential
        from azure.communication.chat._shared.user_token_refresh_options import CommunicationTokenRefreshOptions

        refresh_options = CommunicationTokenRefreshOptions(self.token)
        chat_client = ChatClient(self.endpoint, CommunicationTokenCredential(refresh_options))
        chat_thread_client = chat_client.get_chat_thread_client(self._thread_id)
        # [END get_chat_thread_client]

        print("chat_thread_client created with thread id: ", chat_thread_client.thread_id)

    def get_thread(self):
        # [START get_thread]
        from azure.communication.chat import ChatClient
        from azure.communication.identity._shared.user_credential import CommunicationTokenCredential
        from azure.communication.chat._shared.user_token_refresh_options import CommunicationTokenRefreshOptions

        refresh_options = CommunicationTokenRefreshOptions(self.token)
        chat_client = ChatClient(self.endpoint, CommunicationTokenCredential(refresh_options))
        chat_thread = chat_client.get_chat_thread(self._thread_id)
        # [END get_thread]

        print("get_thread succeeded, thread id: " + chat_thread.id + ", thread topic: " + chat_thread.topic)

    def list_threads(self):
        # [START list_threads]
        from azure.communication.chat import ChatClient
        from azure.communication.identity._shared.user_credential import CommunicationTokenCredential
        from azure.communication.chat._shared.user_token_refresh_options import CommunicationTokenRefreshOptions
        from datetime import datetime, timedelta
        import pytz

        refresh_options = CommunicationTokenRefreshOptions(self.token)
        chat_client = ChatClient(self.endpoint, CommunicationTokenCredential(refresh_options))
        start_time = datetime.utcnow() - timedelta(days=2)
        start_time = start_time.replace(tzinfo=pytz.utc)
        chat_thread_infos = chat_client.list_chat_threads(results_per_page=5, start_time=start_time)

        print("list_threads succeeded with results_per_page is 5, and were created since 2 days ago.")
        for chat_thread_info_page in chat_thread_infos.by_page():
            for chat_thread_info in chat_thread_info_page:
                print("thread id:", chat_thread_info.id)
        # [END list_threads]

    def delete_thread(self):
        # [START delete_thread]
        from azure.communication.chat import ChatClient
        from azure.communication.identity._shared.user_credential import CommunicationTokenCredential
        from azure.communication.chat._shared.user_token_refresh_options import CommunicationTokenRefreshOptions

        refresh_options = CommunicationTokenRefreshOptions(self.token)
        chat_client = ChatClient(self.endpoint, CommunicationTokenCredential(refresh_options))
        chat_client.delete_chat_thread(self._thread_id)
        # [END delete_thread]

        print("delete_thread succeeded")

    def clean_up(self):
        print("cleaning up: deleting created user.")
        self.identity_client.delete_user(self.user)


if __name__ == '__main__':
    sample = ChatClientSamples()
    sample.create_chat_client()
    sample.create_thread()
    sample.get_chat_thread_client()
    sample.get_thread()
    sample.list_threads()
    sample.delete_thread()
    sample.clean_up()
