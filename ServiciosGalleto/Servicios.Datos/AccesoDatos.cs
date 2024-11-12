using Microsoft.EntityFrameworkCore;

namespace Servicios.Datos
{
    public class AccesoDatos : DbContext
    {
        public AccesoDatos(DbContextOptions<AccesoDatos> options) : base(options)
        {
            this.ChangeTracker.LazyLoadingEnabled = false;
        }
    }
}
