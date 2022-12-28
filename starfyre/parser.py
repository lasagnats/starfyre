from html.parser import HTMLParser
from dataclasses import dataclass

from .component import Component


class Parser(HTMLParser):
    stack = []

    def handle_starttag(self, tag, attrs):
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]

        self.stack.append(Component(tag, props, [], {}))

    def handle_endtag(self, tag):

        children = []
        while self.stack:
            node = self.stack[-1]
            if isinstance(node, Component) and node.tag == tag:
                break

            self.stack.pop()
            children.append(node)

        children = children[::-1]
        if self.stack:
            self.stack[-1].children = children

        print("Encountered an end tag :", self.stack)

    def handle_data(self, data):
        self.stack.append(Component("TEXT_NODE", {}, [], {}, data=data))

    def parse(self):
        return self.stack

