# observability-toolkit

[![PyPI - Version](https://img.shields.io/pypi/v/observability-toolkit.svg)](https://pypi.org/project/observability-toolkit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/observability-toolkit.svg)](https://pypi.org/project/observability-toolkit)
[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
-----

Observability patterns for python applications.


*No dependencies outside of standard python libraries*


## Table of Contents

- [Installation](#installation)
- [Examples](#examples)
- [License](#license)

## Installation

```console
pip install observability-toolkit
```


## License

`observability-toolkit` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.


## Future Scope

The following is an excerpt from a conversation with an LLM around what the
features of this library should be:

#### Core Observability Components
1. Metrics collection and reporting
    - Ability to collect and expose application metrics
    - Integration with metrics systems like Prometheus
2. Logging capabilities
    - Standardized logging implementation
    - Support for different log levels (e.g. debug, info, warning, error)
    - Ability to configure log output destinations
3. Tracing and distributed tracing
    - Support for collecting and analyzing trace data
    - Integration with OpenTelemetry or other tracing standards
#### Data Collection and Instrumentation
1. Automatic instrumentation
    - Ability to automatically instrument common Python frameworks and libraries
2.  Manual instrumentation APIs
    - Easy-to-use APIs for manually adding observability to specific parts of the application
3. Context propagation
    - Ability to propagate context across different components and services
#### Configuration and Customization
1. Flexible configuration options
    - Ability to customize various aspects of observability collection and reporting
2. Pluggable architecture
    - Support for custom plugins/extensions to integrate with different systems
3. Sampling and filtering
    - Options for sampling and filtering telemetry data to manage volume and performance impact
#### Developer Experience
1. Easy integration
    - Simple setup process for integrating the toolkit into existing applications
2. Documentation and examples
    - Clear guides on usage and best practices
    - Sample implementations for reference
