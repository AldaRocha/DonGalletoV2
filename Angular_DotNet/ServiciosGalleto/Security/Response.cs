using System;
using System.Collections.Generic;
using System.Text;

namespace Security
{
    public class Response
    {
        public string Message { get; set; }
        public dynamic Token { get; set; }
        public bool headers { get; set; }
        public int PartialContent = 206;
        public int OK = 200;
        public int NotFound = 404;
        public int BadRequest = 403;
        public int Unauthorized = 401;
        private bool Dev { get; set; }
        private Firewall firewall = new Firewall();

        public Response(bool dev = true)
        {
            this.Dev = dev;
            this.firewall = new Firewall();
        }

        public bool IsJWE()
        {
            if (this.headers)
            {
                return true;
            }
            return false;
        }

        public Response Ok(string message, dynamic data = null)
        {
            if (message != "")
            {
                this.Message = message;
            }
            if (data != null)
            {
                if (!this.Dev)
                {
                    this.Token = data;
                }
                else
                {
                    if (this.headers)
                    {
                        this.Token = this.firewall.EncodeJWE(data);
                    }
                    else
                    {
                        this.Token = this.firewall.Encode(data);
                    }
                }
            }
            return this;
        }

        public Response Error(string message)
        {
            if (message != "")
            {
                this.Message = message;
            }
            return this;
        }
    }
}
