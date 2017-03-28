"""
You can run this example like this:
    .. code:: console
            $ luigi --module examples.hello_world examples.HelloWorldTask --local-scheduler
If that does not work, see :ref:`CommandLine`.
"""

import luigi
from luigi import six

class InputText(luigi.ExternalTask):
    """
    This class represents something that was created elsewhere by an external process,
    so all we want to do is to implement the output method.
    """
    date = luigi.DateParameter()

    def output(self):
        """
        Returns the target output for this task.
        In this case, it expects a file to be present in the local file system.
        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget("wc.txt")
        #return luigi.LocalTarget(self.date.strftime('/var/tmp/text/%Y-%m-%d.txt'))


class WordCount(luigi.Task):
    date_interval = luigi.DateIntervalParameter()

    def requires(self):
        """
        This task's dependencies:
        * :py:class:`~.InputText`
        :return: list of object (:py:class:`luigi.task.Task`)
        """
        return [InputText(date) for date in self.date_interval.dates()]

    def output(self):
        """
        Returns the target output for this task.
        In this case, a successful execution of this task will create a file on the local filesystem.
        :return: the target output for this task.
        :rtype: object (:py:class:`luigi.target.Target`)
        """
        return luigi.LocalTarget('%s.txt' % self.date_interval)

    def run(self):
        """
        1. count the words for each of the :py:meth:`~.InputText.output` targets created by :py:class:`~.InputText`
        2. write the count into the :py:meth:`~.WordCount.output` target
        """
        count = {}

        # NOTE: self.input() actually returns an element for the InputText.output() target
        for f in self.input():  # The input() method is a wrapper around requires() that returns Target objects
            for line in f.open('r'):  # Target objects are a file system/format abstraction and this will return a file stream object
                for word in line.strip().split():
                    count[word] = count.get(word, 0) + 1

        # output data
        f = self.output().open('w')
        for word, count in six.iteritems(count):
            f.write("%s\t%d\n" % (word, count))
        f.close()  # WARNING: file system operations are atomic therefore if you don't close the file you lose all data



class HelloWorldTask(luigi.Task):
    task_namespace = "examples"
    test_str = luigi.Parameter(default=10)

    def run(self):
        msg = "@@@ {task} @@@ : Hello, world!".format(task=self.__class__.__name__)
        w = self.output().open('w')
        w.write(msg)
        w.close()
        print(msg)

    def output(self):
        return luigi.LocalTarget("/var/tmp/test/test.txt")

if __name__ == '__main__':
    # python lgwc.py WordCount --date-interval 2017-03-05
    # python lg.py HelloWorldTask
    luigi.run()
    # luigi.run(['examples.HelloWorldTask', '--workers', '1', '--local-scheduler'])
