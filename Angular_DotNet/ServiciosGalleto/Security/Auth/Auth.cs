using Security.Partial;
using Servicios.Datos;
using Servicios.Entidad.Tables;
using System.Linq;

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
            UsuarioLogin data = request.getData<UsuarioLogin>();
            Usuario usuario = this.DbContext.Usuario.Where(p => p.Pin.Equals(data.Pin)).FirstOrDefault();

            if (usuario == null)
            {
                return new ResponseInterface("Verifica que el pin sea correcto", response.PartialContent, true);
            }

            AuthData auth = new AuthData(usuario);

            Bearer bearer = new Bearer
            {
                UsuarioId = usuario.UsuarioId
            };
            auth.Bearer = this.firewall.Encode(bearer);

            return new ResponseInterface("", response.OK, false, auth);
        }
    }
}
