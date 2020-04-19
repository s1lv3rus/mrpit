import requests
import vk_api

vk_session = vk_api.VkApi('john_k@inbox.ru', 'Ggoogle555556')
vk_session.auth()

vk = vk_session.get_api()

friends = vk.friends.get()


# for friend in friends['items'][85:90]:
#     vk.groups.invite(group_id='192640830', user_id=friend)
#     print(friend)



#
# invites = vk.groups.getInvitedUsers(group_id='192640830')
# print(invites)
