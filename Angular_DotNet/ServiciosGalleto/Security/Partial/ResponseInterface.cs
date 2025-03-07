using System;
using System.Collections.Generic;
using System.Text;

namespace Security.Partial
{
    public class ResponseInterface
    {
        public AuthData authData;
        public string message;
        public int status;
        public bool error;

        public ResponseInterface(string message, int status, bool error, dynamic authData = null)
        {
            this.authData = authData;
            this.message = message;
            this.status = status;
            this.error = error;
        }
    }
}
