# -*- coding: utf-8 -*-
"""
@File    : MenuHelper.py
@Time    : 2019-08-29 17:51
@Author  : 杨小林
废弃没用的
"""
class MenuHelper(object):
    def __init__(self, request):
        # 当前请求的request对象
        self.request = request
        # 当前用户名
        self.username = username
        # 当前url,如用户访问127.0.0.1：8000/index.html?p=123 会获得：index.html
        self.current_url = request.path_info

        # 当前用户的所有权限
        self.permission2action_dict = None
        # 当前用户菜单中显示的所有权限（叶子节点）
        self.menu_leaf_list = None
        # 所有菜单
        self.menu_list = None

        self.session_data()

    def session_data(self):
        permission_dict = self.request.session.get('permission_info')
        if permission_dict:
            self.permission2action_dict = permission_dict['permission2action_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']
        else:
            # 获取当前用户的角色列表
            role_list = models.Role.objects.filter(user2role__u__username=self.username)

            # 获取当前用户的权限列表(url+action)
            permission2action_list = models.Permission2Action.objects.\
                filter(permission2action2role__r__in=role_list).\
                values('p__url', 'a__code').distinct()

            permission2action_dict = {}
            for item in permission2action_list:
                if item['p__url'] in permission2action_dict:
                    permission2action_dict[item['p__url']].append(item['a__code'])
                else:
                    permission2action_dict[item['p__url']] = [item['a__code'], ]

            # 获取菜单的叶子节点，即：菜单的最后一层应该显示的权限
            menu_leaf_list = list(models.Permission2Action.objects.
                                  filter(permission2action2role__r__in=role_list).
                                  exclude(p__menu__isnull=True).
                                  values('p_id', 'p__url', 'p__caption', 'p__menu').distinct())

            # 获取所有菜单列表
            menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))

            self.request.session['permission_info'] = {
                'permission2action_dict': permission2action_dict,
                'menu_leaf_list': menu_leaf_list,
                'menu_list': menu_list,
            }

            # self.permission2action_list = permission2action_list
            # self.menu_leaf_list = menu_leaf_list
            # self.menu_list = menu_list

    def menu_data_list(self):
        # 设置一个空的叶子节点字典
        menu_leaf_dict = {}
        # 首先设置叶子父id节点为空
        open_left_parent_id = None

        for item in self.menu_leaf_list:
            # 将获取的叶子节点列表的每一个值转换为字典形式，并重新设置key，添加child，status，open字段
            item = {
                'id': item['p_id'],
                'url': item['p__url'],
                'caption': item['p__caption'],
                'parent_id': item['p__menu'],
                'child': [],
                'status': True,  # 是否显示
                'open': False,  # 是否打开
            }
            # 判断每一个叶子节点的父节点，将每个叶子节点的内容添加至父节点id作为的key中
            # 判断父节点id作为的key是否在叶子节点字典中存在，如果存在，则将item值append进入
            if item['parent_id'] in menu_leaf_dict:
                menu_leaf_dict[item['parent_id']].append(item)
            # 如果不存在，则直接在列表中生成一个key是叶子节点父节点id的，值为item的数据
            else:
                menu_leaf_dict[item['parent_id']] = [item, ]

            # 判断用户输入的url是否与现在的url匹配，item['url']可以写成一个正则表达式，用match进行匹配
            # 如果匹配上，将叶子节点的open置为true，并将叶子节点的父节点id进行赋值
            import re
            if re.match(item['url'], self.current_url):
                item['open'] = True
                open_left_parent_id = item['parent_id']

        # 设置一个菜单空字典
        menu_dict = {}

        # 将菜单列表转换为字典，并增加child，status，open字段
        # 将列表中的id作为key，列表中的值作为值
        for item in self.menu_list:
            item['child'] = []
            item['status'] = False
            item['open'] = False
            menu_dict[item['id']] = item

        # 循环叶子字典，设置菜单字典中对应的child内容为叶子字典的值
        for k, v in menu_leaf_dict.items():
            menu_dict[k]['child'] = v
            # 设置菜单字典的parent_id的值为叶子字典的key（也就是叶子中的parent）
            parent_id = k
            # 设置菜单字典中的status状态为True，并循环设置父级菜单的status为True
            while parent_id:
                menu_dict[parent_id]['status'] = True
                parent_id = menu_dict[parent_id]['parent_id']

        # 判断叶子父级id，将open设置为True，并循环设置父级菜单的open为True
        while open_left_parent_id:
            menu_dict[open_left_parent_id]['open'] = True
            open_left_parent_id = menu_dict[open_left_parent_id]['parent_id']

        # print('循环权限用户url字典，将用户权限取得的id匹配菜单列表id并设置["child"]值为用户权限内容')
        # print('设置parent_id变量为：用户权限url的id')
        # print('如果有，菜单id的["status"]设置为True')
        # print('并且将parent_id的值设置为：菜单字典中菜单id的["parent"]，等待下一次循环')
        # for k, v in menu_dict.items():
        #     print(k, v)
        # #####################处理菜单的等级关系#########################
        # menu_dict 应用：多级评论，多级菜单

        result = []
        # 按父子关系，将菜单列表中的值，层叠放入一个result中
        # 这里需要注意的是，只需要寻找一层的父id，并将自己放入，无需一层一层寻找到上一层的父节点。
        for row in menu_dict.values():
            if not row['parent_id']:
                result.append(row)
            else:
                menu_dict[row['parent_id']]['child'].append(row)

        return result

    def menu_content(self, child_list):

        response = ''
        tpl = """
            <div class="item %s">
                <div class="title">%s</div>
                <div class="content">%s</div>
            </div>
        """
        for row in child_list:
            if not row['status']:
                continue
            active = ''
            if row['open']:
                active = 'active'
            if 'url' in row:
                response += '<a class="%s" href="%s">%s</a>' % (active, row['url'], row['caption'])
            else:
                title = row['caption']
                content = self.menu_content(row['child'])
                response += tpl % (active, title, content)

        return response

    def menu_tree(self):
        response = ''
        tpl = """
            <div class="item %s">
                <div class="title">%s</div>
                <div class="content">%s</div>
            </div>
        """
        for row in self.menu_data_list():
            if not row['status']:
                continue
            active = ''
            if row['open']:
                active = 'active'
            title = row['caption']
            content = self.menu_content(row['child'])
            response += tpl % (active, title, content)

        return response

    def action(self):
        """
        检查当前用户是否对当前URL有访问权，并获取对当前URL有什么权限
        :return:
        """

        action_list = []

        for k, v in self.permission2action_dict.items():
            if re.match(k, self.current_url):
                action_list = v
                break

        return action_list