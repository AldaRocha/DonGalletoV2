using Servicios.Datos;
using Servicios.Entidad.Model;
using System.Collections.Generic;
using System.Linq;

namespace Servicios.Fachada.DAO
{
    public class MedidaDAO
    {
        public List<Medida> GetAllMedida(AccesoDatos DbContext)
        {
            return DbContext.Medida.ToList();
        }
    }
}
