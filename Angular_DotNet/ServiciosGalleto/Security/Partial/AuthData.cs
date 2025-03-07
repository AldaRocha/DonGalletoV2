using Servicios.Entidad.Tables;

namespace Security.Partial
{
    public class AuthData
    {
        public string Nombre { get; set; }
        public string Bearer { get; set; }

        public AuthData(Usuario usuario)
        {
            this.Nombre = usuario.Nombre;
        }
    }
}
