import boto3
import datetime
from typing import List
from enum import Enum


class MetricUnit(Enum):
    NONE = "None"
    # measures
    PERCENT = "Percent"
    COUNT = "Count"
    # durations
    MICROSECONDS = "Microseconds"
    MILLISECONDS = "Milliseconds"
    # size
    BYTES = "Bytes"
    KILOBYTES = "Kilobytes"
    MEGABYTES = "Megabytes"
    GIGABYTES = "Gigabytes"
    TERABYTES = "Terabytes"
    BITS = "Bits"
    # throughput
    BITS_P_SECOND = "Bytes/Second"
    KILOBITS_P_SECOND = "Kilobytes/Second"
    MEGABITS_P_SECOND = "Megabytes/Second"
    GIGABITS_P_SECOND = "Gigabytes/Second"
    TERABITS_P_SECOND = "Terabits/Second"
    COUNTS_P_SECOND = "Count/Second"


class MetricStatistics:
    def __init__(self, sample_count: int, sum: float, minimum: float, maximum: float):
        """
        The statistical values for a metric.
        :param sample_count: The number of samples used for the statistic set.
        :param sum: The sum of values for the sample set.
        :param minimum: The minimum value of the sample set.
        :param maximum: The maximum value of the sample set.
        """
        self.sample_count = sample_count
        self.sum = sum
        self.minimum = minimum
        self.maximum = maximum

    def to_obj(self) -> object:
        return {
            "SampleCount": 123.0,
            "Sum": 123.0,
            "Minimum": 123.0,
            "Maximum": 123.0,
        }


class MetricDimension:
    def __init__(self, name: str, value: str):
        """
        A dimension is a name/value pair that is part of the identity of a metric.
        Every metric has specific characteristics that describe it, and you can think of dimensions as categories for
        those characteristics. Dimensions help you design a structure for your statistics plan.

        Examples:
            name: 'PURCHASE_SERVICE'
            value: 'MyCoolService'

            name: 'APP_VERSION'
            value: '1.0'

        :param name: The name of the dimension.
        :param value: The value representing the dimension measurement.
        """
        self.name = name
        self.value = value

    def to_obj(self) -> object:
        return {"Name": self.name, "Value": self.value}


class CloudWatchMetric:
    """
    The namespace for the metric data.
    To avoid conflicts with AWS service namespaces, you should not specify a namespace that begins with AWS/
    """

    __namespace = "CUSTOM/metrics"

    def __init__(self):
        self.client = client = boto3.client("cloudwatch")

    def submit(
        self,
        metric_name: str,
        value: float,
        dimensions: List[MetricDimension] = None,
        values: List[float] = None,
        counts: List[int] = None,
        statistics: MetricStatistics = None,
        unit: MetricUnit = MetricUnit.NONE,
        timestamp=datetime.datetime.now(),
    ):
        """
        :param metric_name: The name of the metric.
        :param value: The value for the metric. Values must be in the range of -2^360 to 2^360.
                      Special values like NaN, +Infinity, -Infinity are not supported.
        :param dimensions: A dimension is a name/value pair that is part of the identity of a metric.
                           Describe categories of metric characteristics.
        :param values: Array of numbers representing the values for the metric during the period.
        :param counts: Array of numbers that is used along with the Values array. Each number in the Count array is the
                       number of times the corresponding value in the Values array occurred during the period.
        :param statistics: The statistical values for the metric.
        :param unit:
        :param timestamp: The time the metric data was received. Expressed as a UNIX timestamp.
        """

        assert not counts or values and counts, (
            "Counts refers to the number of times the corresponding value "
            "in the values array occurred during the period."
        )
        assert not counts or len(counts) == len(
            values
        ), "Counts must include the same amount of values as the Values array."

        metric_data = {
            "MetricName": metric_name,
            "Timestamp": timestamp,
            "Value": value,
            "Unit": unit.value,
            # "StorageResolution": 123,
        }

        if dimensions:
            metric_data["Dimensions"] = [d.to_obj() for d in dimensions]

        if values:
            metric_data["Values"] = values

        if counts:
            metric_data["Counts"] = counts

        if statistics:
            metric_data["StatisticValues"] = statistics.to_obj()

        response = self.client.put_metric_data(
            Namespace=self.__namespace, MetricData=[metric_data,],
        )
        print(response)
        if not response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            pass


if __name__ == "__main__":
    cw = CloudWatchMetric()
    cw.submit("MyCustomMetric", 1500.1337, [MetricDimension("API_VERSION", "0.0.BETA")])
