from random import seed
from random import randrange
from csv import reader
from math import sqrt

class randomForest:
    def __init__(self):
        print('随机森林开始')
        print(seed(1))

    def load_csv(self, filename):
        dataset = list()
        with open(filename, 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if not row:
                    continue
                dataset.append(row)
        return dataset

    # Convert string column to integer
    def str_column_to_integer(self, dataset, column):
        for row in dataset:
            row[column] = int(row[column].strip())

    # Convert String column to integer
    def str_column_to_int(self, dataset, column):
        class_values = [row[column] for row in dataset]
        unique = set(class_values)
        lookup = dict()
        # enumerate()用于将一个可遍历的数据对象组合成一个索引序列
        for i, value in enumerate(unique):
            lookup[value] = i
        for row in dataset:
            row[column] = lookup[row[column]]
        return lookup

    # 创建随机子样本
    def subsample(self, dataset, ratio):
        sample = list()
        # round()方法返回浮点数x的四舍五入值
        n_sample = round(len(dataset) * ratio)
        while len(sample) < n_sample:
            # 有放回的随机采样，有一些样本被重复采样，从而在训练集中多次出现，有的则从未在训练集中出现。
            # 此方法即为自助采样法，从而保证每颗决策树训练集的差异性
            index = randrange(len(dataset))
            sample.append(dataset[index])
        return sample

    # 根据特征和特征值分割数据集
    def test_split(self, index, value, dataset):
        left, right = list(), list()
        for row in dataset:
            if row[index] < value:
                left.append(row)
            else:
                right.append(row)
        return left, right

    # 计算基尼指数
    def gini_index(self, groups, class_values):
        gini = 0.0
        # print(groups)
        # print(len(class_values))输出：166
        for class_value in class_values:
            for group in groups:
                size = len(group)
                if size == 0:
                    continue
                # print(class_value)输出：{'M'}
                # print(group)
                # exit()
                # print(size)输出：109
                # list count()统计某个元素出现在列表中的次数
                proportion = [row[-1] for row in group].count(class_value) / float(size)
                # print(proportion)
                gini += (proportion * (1.0 - proportion))
        return gini

    # Select the best split point for a dataset
    # 找出分割数据集的最优特征，得到最优的特征index,特征值row[index],以及分割完的数据groups(left,right)
    def get_split(self, dataset, n_features):
        # class_values =[0,1]
        class_values = list(set(row[-1]) for row in dataset)
        b_index, b_value, b_score, b_group = 999, 999, 999, None
        features = list()
        # n_features特征值
        while len(features) < n_features:
            # 往features添加n_features个特征(n_features等于特征数的根号)，特征索引从dataset中随机取
            index = randrange(len(dataset[0]) - 1)
            if index not in features:
                features.append(index)

        # 在n_features个特征中选出最优的特征索引，并没有遍历所有特征，从而保证每个决策树的差异
        for index in features:
            for row in dataset:
                # groups = (left, right);row[index]遍历每一行index索引下的特征值作为分类值values,
                # 找出最优的分类特征和特征值
                groups = self.test_split(index, row[index], dataset)
                # print(groups)输出格式：[[]],[[]]
                gini = self.gini_index(groups, class_values)
                # print(gini)
                if gini < b_score:
                    # 最后得到最优的分类特征b_index,分类特征值b_value,分类结果b_groups。 b_value为分错的代价成本
                    b_index, b_value, b_score, b_groups = index, row[index], gini, groups
        return {'index': b_index, 'value': b_value, 'groups': b_groups}

    # 创建一个终端节点, 输出group中出现次数最多的标签
    def to_terminal(self, group):
        outcomes = [row[-1] for row in group]
        # max()函数中，当key函数不为空时，就以key的函数对象为判断的标准
        # print(outcomes)
        return max(set(outcomes), key=outcomes.count)

    # 创建子分割器，递归分类，直到分类结束
    def split(self, node, max_depth, min_size, n_features, depth):
        # max_depth = 10 ,min_size = 1, n_features = int(sqrt(len(dataset[0])) - 1)
        left, right = node['groups']
        del (node['groups'])
        # 检查左右分支
        if not left or not right:
            node['left'] = node['right'] = self.to_terminal(left + right)
            return

        # 检查迭代次数,表示递归十次后，若分类还没结束，则选取数据中分类标签较多的作为结果，使分类提前结束，防止过拟合。
        if depth >= max_depth:
            node['left'], node['right'] = self.to_terminal(left), self.to_terminal(right)

        # 加工左子树
        if len(left) <= min_size:
            node['left'] = self.to_terminal(left)
        else:
            # print('左子树递归')
            # node['left']是一个字典，形式为{'index':b_index,'value':b_value,'groups':b_groups},所以node是一个多层字典
            node['left'] = self.get_split(left, n_features)
            # 递归，depth+1计算递归层数
            self.split(node['left'], max_depth, min_size, n_features, depth + 1)

        # 加工右子树
        if len(right) <= min_size:
            node['right'] = self.to_terminal(right)
        else:
            # print('右子树递归')
            node['right'] = self.get_split(right, n_features)
            self.split(node['right'], max_depth, min_size, n_features, depth + 1)

    # build a decision tree，建立一个决策树
    def build_tree(self, train, max_depth, min_size, n_features):

        # 找出最优的分割点
        root = self.get_split(train, n_features)
        # print(root)
        # 创建子分类器，递归分类，直到分类结束。
        self.split(root, max_depth, min_size, n_features, 1)
        return root
        # exit()

    # 用决策树进行预测，预测模型的分类结果
    def predict(self, node, row):
        if row[node['index']] < node['value']:
            if isinstance(node['left'], dict):
                return self.predict(node['left'], row)
            else:
                return node['left']
        else:
            if isinstance(node['right'], dict):
                return self.predict(node['right'], row)
            else:
                return node['right']

    # 用一系列的套袋树进行预测
    def bagging_predict(self, trees, row):
        # 使用多个决策树trees对测试集test的第row行进行预测，再使用简单投票法判断出该行所属的分类
        predictions = [self.predict(tree, row) for tree in trees]
        return max(set(predictions), key=predictions.count)

    # Random Forest Algorithm，随机森林算法
    def random_forest(self, train, test, max_depth, min_size, sample_size, n_trees, n_features):
        trees = list()
        # n_trees表示决策树的数量
        for i in range(n_trees):
            # 随机采样，保证每颗决策树训练集的差异性
            # sample_size采样速率
            print('训练集长度=', len(train))
            # 创建随机子样本
            sample = self.subsample(train, sample_size)
            # 建立一个决策树
            tree = self.build_tree(sample, max_depth, min_size, n_features)
            trees.append(tree)
        ##用一系列的套袋树进行预测
        predictions = [self.bagging_predict(trees, row) for row in test]
        # print(predictions)
        return (predictions)

    # Split a dataset into k folds
    '''
    将数量集dataset分成n_flods份，每份包含len(dataset)/ n_folds个值，每个值由dataset数据集的内容随机产生，每个值被调用一次
    '''

    def cross_validation_split(self, dataset, n_folds):
        dataset_split = list()
        # 复制一份dataset，防止dataset的内容改变
        dataset_copy = list(dataset)
        # 每份的数据量
        fold_size = len(dataset) / n_folds
        # print(dataset_copy)
        print('每份的长度', fold_size)
        print('dataset_copy长度=', len(dataset_copy))

        for i in range(n_folds):
            # 每次循环fold清零，防止重复导入dataset_split
            fold = list()
            # 随机抽取数据，不断地往fold中添加数据
            while len(fold) < fold_size:
                # 指定递增基数集合中的一个随机数，基数缺省值为1
                # print('dataset长度=',len(dataset_copy))
                if (len(dataset_copy) == 0):
                    break
                index = randrange(len(dataset_copy))
                # 将对应索引index的内容从dataset_copy中导出，并将该内容从dataset_copy中删除。
                # pop()函数用于移除列表中的一个元素，并返回该元素的值。
                fold.append(dataset_copy.pop(index))
                # print(len(fold))
            dataset_split.append(fold)
            #print('i===', i)
        # dataset分割出的n_flods个数据构成的列表，为了用于交叉验证
        return dataset_split

    # 计算精度百分比,导入实际值和预测值，计算精确度
    def accuracy_metric(self, actual, predicted):
        correct = 0
        for i in range(len(actual)):
            if actual[i] == predicted[i]:
                correct += 1
        return correct / float(len(actual)) * 100.0

    def evaluate_algorithm(self, dataset, algorithm, n_folds, *args):
        folds = self.cross_validation_split(dataset, n_folds)
        scores = list()
        # 每次循环从folds取出一个fold作为测试集，其余作为训练集，遍历整个folds，实现交叉验证
        for fold in folds:
            train_set = list(folds)
            train_set.remove(fold)
            # sum三维向量转二维数组，将多个fold组合成一个train_set列表
            train_set = sum(train_set, [])
            test_set = list()
            # fold表示从原始数据集dataset提取出来的测试集
            for row in fold:
                row_copy = list(row)
                test_set.append(row_copy)
                row_copy[-1] = None
            predicted = algorithm(train_set, test_set, *args)
            print('交叉验证RF的预测值=', predicted)
            actual = [row[-1] for row in fold]
            print('实际的值=', actual)
            accuracy = self.accuracy_metric(actual, predicted)
            scores.append(accuracy)
        return scores


if __name__ == '__main__':
    rf = randomForest()
    #filename = './sonar.all-data'
    filename = './mnt/5/trainData/trainData.txt'
    dataset = rf.load_csv(filename)
    print(len(dataset))
    #print(dataset)

    # 整个矩阵，按列从左到右转化
    for i in range(0, len(dataset[0]) - 1):
        rf.str_column_to_integer(dataset, i)  # 将str类型转变为integer
    print(dataset)
    # 将最后一列表示表示标签的值转化为Int类型0,1
    # str_column_to_int(dataset, len(dataset[0]) - 1 )
    # evaluate algorithm算法评估
    # 分成5份，进行交叉验证
    n_folds = 5

    # 迭代次数
    max_depth = 10
    min_size = 1
    sample_size = 2
    # 调参，TODO，准确性与多样性之间的权衡
    #n_features = 15
    n_features = int(sqrt(len(dataset[0]) - 1))
    # 随机森林的树的选择，理论上越多越好
    for n_trees in [1, 3]:
        # python中将函数作为另一个函数的参数传入
        scores = rf.evaluate_algorithm(dataset, rf.random_forest, n_folds, max_depth, min_size, sample_size, n_trees, n_features)
        print('Trees:%d' % n_trees)
        print('Scores:%s' % scores)
        print('Mean Accuracy: %.3f%%' % (sum(scores) / float(len(scores))))
        exit()
