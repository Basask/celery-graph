# -*- coding: utf-8 -*-
# @Date    : 2016-04-18 15:32:08
# @Author  : Rafael Fernandes (basask@collabo.com.br)
# @Link    : http://www.collabo.com.br/

from __future__ import unicode_literals

from celery import signature
from celery import chord


class IGraphBuilder(object):

    def __init__(self, graph):
        self.graph = graph

    def get_signature(self):
        return self.build_signature(self.graph.vs[0])

    @classmethod
    def find_vertex_by_type(cls, vertex, lookup):
        if vertex['type'] == lookup:
            return vertex
        for sub in vertex.successors():
            ret = cls.find_vertex_by_type(sub, lookup)
            if ret is not None:
                return ret
        return None

    @staticmethod
    def create_signature(vertex):
        task_name = 'tasks.{}.{}'.format(
            vertex['domain'],
            vertex['id']
        )
        task_config = vertex['parameters']
        return signature(task_name, kwargs=task_config)

    def build_chord_signature(self, vertex):

        end_vertex = self.find_vertex_by_type(vertex, 'join')
        end_signature = self.get_first_successor_signature(end_vertex)

        sub_signatures = []
        for sub in vertex.successors():
            sub_signature = self.build_signature(sub)
            if sub_signature:
                sub_signatures.append(sub_signature)
        return chord(sub_signatures, end_signature)

    def build_chain_signature(self, vertex):
        base = self.create_signature(vertex)
        return reduce(lambda a, b: a | self.build_signature(b), vertex.successors(), base)

    def get_first_successor_signature(self, vertex):
        return self.build_signature(vertex.successors()[0])

    def build_signature(self, vertex):

        if vertex['type'] == 'virtual':
            return self.get_first_successor_signature(vertex)

        if vertex['type'] == 'split':
            return self.build_chord_signature(vertex)

        if vertex['type'] == 'join':
            return None

        task_list = vertex.successors()
        this_signature = self.create_signature(vertex)
        if len(task_list):
            next_signature = self.get_first_successor_signature(vertex)
            if next_signature:
                this_signature |= next_signature
        return this_signature
