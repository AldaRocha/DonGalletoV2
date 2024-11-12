using Security.Partial;
using Servicios.Datos;

namespace Security.Auth
{
    public class Auth
    {
        RequestInterface request;
        AccesoDatos DbContext;
        Firewall firewall;

        public Auth(AccesoDatos DbContext, RequestInterface request)
        {
            this.request = request;
            this.firewall = new Firewall();
            this.DbContext = DbContext;
        }

        public ResponseInterface Connect(Response response, bool JWE = false)
        {
            return new ResponseInterface("", response.OK, false);
        }

        public ResponseInterface Logout(Response response)
        {
            return new ResponseInterface("", response.OK, false);
        }
    }
}
