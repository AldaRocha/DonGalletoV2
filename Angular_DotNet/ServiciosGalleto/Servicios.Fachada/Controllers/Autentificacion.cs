using Microsoft.AspNetCore.Http;
using Security.Partial;
using Security;
using Servicios.Datos;

namespace Servicios.Fachada.Controllers
{
    public class Autentificacion
    {
        public static readonly string mensajeNoAutentificado = "No tienes permiso para realizar esta petición.";

        public Autentificacion(AccesoDatos DbContext)
        {
        }

        public static Bearer GetUsuarioToken(IHeaderDictionary headers)
        {
            var header = headers["Authorization"];

            Firewall firewall = new Firewall();
            Bearer usuarioToken = firewall.Decode<Bearer>(header);

            return usuarioToken;
        }
    }
}
