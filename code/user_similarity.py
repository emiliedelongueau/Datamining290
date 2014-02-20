# Emilie de Longueau
# HMK Map Reduce Job : user_similarity.py


from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    
    def extract_user_biz(self, _, record):
        """Take in a record, yield <user_id, business_id>"""
        if record['type'] == 'review':
            yield [ record['user_id'], record['business_id'] ]

    def user_list_business_ids(self, user_id, business_ids):
        """Yield the user_id and the list of businessed reviewed"""
        yield [user_id, list(business_ids)]




    def aggregate_biz(self, user_id, business_ids):
        """Group user_id/business_ids together by the "BIZ" text"""
        yield ["BIZ", [user_id, business_ids]]

    def unique_list_user_business_ids(self, text, user_business_ids):
        """Yield the entire list of pairs user_id/bsuiness_ids"""
        yield [text, list(user_business_ids)]




    def paired_users(self, stat, user_business_ids):
        """Yield the list of 2 user_id as key and the concatenation of the 2 correponding business_ids lists as value"""
        for i in user_business_ids:
            for j in user_business_ids: # doublons
                if user_business_ids.index(j) > user_business_ids.index(i):
                    yield [[i[0], j[0]], [i[1], j[1]]]


    def similarity(self, user_pair, business_id_pair):
        """Yield the user_pair with their Jaccard similarity of businesses reviewed if >=0.5"""
        list_business_id_pair= list(business_id_pair) # convert generator in a list, [0] to get the 2-list pair
        list_business1 = list_business_id_pair[0][0]
        list_business2 = list_business_id_pair[0][1]
        inter = list(set(list_business1) & set(list_business2))
        union = list_business1 + list_business2
        jaccard_sim = float(len(inter)) / len(union)
        if jaccard_sim >= 0.5 :
            yield[user_pair, jaccard_sim]



    def steps(self):
        """Give the user pairs that have whose similarity >= 0.5 (in terms of business reviewed):
        extract_user_biz: <line, record> => <user_id, business_id>
        user_list_business_ids: <user_id, business_id> => <user_id, [business_ids]>
        aggregate_biz: <user_id, [business_ids]> => <'BIZ', [user_id, [business_ids]]>
        unique_list_user_business_ids: <'BIZ', [user_id, [business_ids]]> => <'BIZ', [[user_id, [business_ids], ...]>
        paired_users: <'BIZ', [[user_id, [business_ids], ...]> => <[user_pair], [[business_ids0],[business_ids1]]>
        similarity: <[user_pair], [[business_ids0],[business_ids1]]> => <[user_pair], similarity>=0.5 > 
        """
        return [
            self.mr(self.extract_user_biz, self.user_list_business_ids), 
            self.mr(self.aggregate_biz, self.unique_list_user_business_ids),
            self.mr(self.paired_users, self.similarity),
        ]


if __name__ == '__main__':
    UserSimilarity.run()
