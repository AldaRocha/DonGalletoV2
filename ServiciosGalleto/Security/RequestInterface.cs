using System;
using System.Collections.Generic;
using System.Text;

namespace Security
{
    public class RequestInterface
    {
        public string Token { get; set; }
        private Firewall firewall;

        public RequestInterface()
        {
            this.firewall = new Firewall();
        }

        public T getData<T>(bool JWE = false)
        {
            if (JWE)
            {
                this.firewall.JWE = true;
            }
            return this.firewall.Decode<T>(this.Token);
        }
    }
}
