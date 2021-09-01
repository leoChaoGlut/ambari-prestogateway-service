# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from common import prestoGatewayHome, presto_gateway_jar
from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script


class PrestoGateway(Script):
    def install(self, env):
        Execute('mkdir -p {0}'.format(prestoGatewayHome))

        Execute('wget --no-check-certificate {0} -O {1}'.format(presto_gateway_jar,
                                                                prestoGatewayHome + '/presto-gateway.jar'))

        self.configure(env)

    def stop(self, env):
        Execute('ps -ef |grep -v grep |grep "presto-gateway.jar"|awk \'{print $2}\'|xargs kill -9')

    def start(self, env):
        self.configure(self)

        from params import presto_gateway
        args = ''
        for key, value in presto_gateway.iteritems():
            args += ' --' + key + '=' + value
        Execute('cd ' + prestoGatewayHome + ' && java -jar presto-gateway.jar ' + args + ' > out.pg 2>&1 &')

    def status(self, env):
        try:
            Execute(
                'export PRSETO_GATEWAY_COUNT=`ps -ef |grep -v grep |grep "presto-gateway.jar" | wc -l` && `if [ $PRSETO_GATEWAY_COUNT -ne 0 ];then exit 0;else exit 3;fi `'
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        return


if __name__ == '__main__':
    PrestoGateway().execute()
