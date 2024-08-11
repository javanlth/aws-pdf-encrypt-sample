"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""

from datetime import datetime

from cfnlint.rules import RuleMatch
from cfnlint.rules.resources.lmbd.DeprecatedRuntime import DeprecatedRuntime


class DeprecatedRuntimeUpdate(DeprecatedRuntime):
    """Check if EOL Lambda Function Runtimes are used"""

    id = "E2533"
    shortdesc = "Check if Lambda Function Runtimes are updatable"
    description = (
        "Check if an EOL Lambda Runtime is specified and you cannot update the function"
    )
    source_url = (
        "https://docs.aws.amazon.com/lambda/latest/dg/runtime-support-policy.html"
    )
    tags = ["resources", "lambda", "runtime"]

    def check_runtime(self, runtime_value, path):
        """Check if the given runtime is valid"""
        matches = []

        runtime = self.deprecated_runtimes.get(runtime_value)
        if runtime:
            if (
                datetime.strptime(runtime["update-block"], "%Y-%m-%d")
                < self.current_date
            ):
                message = "Runtime ({0}) was deprecated on {1}. Update disabled on {2}. Please consider updating to {3}"
                matches.append(
                    RuleMatch(
                        path,
                        message.format(
                            runtime_value,
                            runtime["deprecated"],
                            runtime["update-block"],
                            runtime["successor"],
                        ),
                    )
                )
        return matches
