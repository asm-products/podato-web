from flask import current_app as podatoApp
from celery import *
from celery.result import ResultBase, AsyncResult

app = Celery()

app.conf.CELERY_RESULT_BACKEND = podatoApp.config["REDIS_URL"]
app.conf.BROKER_URL = podatoApp.config["REDIS_URL"]
app.conf.CELERY_TRACK_STARTED = True


class AsyncSuccess(object):

    def __init__(self, async_result=None, success=None):
        if async_result != None and success != None:
            raise ValueError("async_result and success shouldn't both be given.")

        if async_result == None and success == None:
            raise ValueError("Either async_result or success must be given.")

        self.id = async_result.id if async_result else None
        self.async_result = async_result
        self._success = success
        self._final_async_result_cache = None

    @property
    def _final_async_result(self):
        if self._final_async_result_cache:
            return self._final_async_result_cache

        if not self.async_result:
            return None

        result = self.async_result
        lastResult = self.async_result
        while True:
            if isinstance(result, ResultBase):
                lastResult = result
                result = result.result
            else:
                return lastResult


    @property
    def success(self):
        if self._success != None:
            return self._success

        return not isinstance(self._final_async_result.result, Exception)

    @property
    def state(self):
        if self._success != None:
            return {True: "SUCCESS", False: "FAILURE"}[self._success]
        return self._final_async_result.state

    @classmethod
    def get(cls, id):
        return cls(async_result=AsyncResult(id))

    def __repr__(self):
        return "<AsyncSuccess #%s success=%s state=%s>" % (self.id, self.success, self.state)