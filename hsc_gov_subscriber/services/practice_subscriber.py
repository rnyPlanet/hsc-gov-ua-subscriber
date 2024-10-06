from hsc_gov_subscriber.services.base.subscriber import HscGovSubscriberAbs
from hsc_gov_subscriber.utils.config import Config


class PracticeSubscriber(HscGovSubscriberAbs):
    async def subscribe(self, text):
        await super().subscribe(text)

    def get_question_id(self):
        return Config.QUESTION_ID.value

    def get_sub_id(self):
        return Config.SUB_ID.value

    def get_reservecherga_data(self, question_id, first_freetime_id):
        return (
            f'------WebKitFormBoundarybjBnn2JwFbBJj5R3\r\nContent-Disposition: form-data; name="question_id"\r\n\r\n{question_id}\r\n'
            f'------WebKitFormBoundarybjBnn2JwFbBJj5R3\r\nContent-Disposition: form-data; name="id_chtime"\r\n\r\n{first_freetime_id}\r\n'
            f'------WebKitFormBoundarybjBnn2JwFbBJj5R3\r\nContent-Disposition: form-data; name="email"\r\n\r\n{Config.EMAIL.value}\r\n'
            f'------WebKitFormBoundarybjBnn2JwFbBJj5R3--\r\n')
