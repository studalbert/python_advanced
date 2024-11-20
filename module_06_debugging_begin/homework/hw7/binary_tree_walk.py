"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""

import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional
from unittest.mock import right

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10**6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    tree_dict = dict()
    with open(path_to_log_file, "r") as file:
        for line in file:
            if "Visiting" in line:
                value = int(re.search(r"\d+", line).group())
                if tree_dict.get(value) is None:
                    tree_dict[value] = BinaryTreeNode(val=value)
            elif "left" in line:
                values = re.findall(r"\d+", line)
                value1 = int(values[0])
                value2 = int(values[1])
                tree_dict[value2] = BinaryTreeNode(val=value2)
                tree_dict[value1].left = tree_dict[value2]
            elif "right" in line:
                values = re.findall(r"\d+", line)
                value1 = int(values[0])
                value2 = int(values[1])
                tree_dict[value2] = BinaryTreeNode(val=value2)
                tree_dict[value1].right = tree_dict[value2]
    return list(tree_dict.values())[0]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_4.txt",
    )

    root = get_tree(7)
    walk(root)
