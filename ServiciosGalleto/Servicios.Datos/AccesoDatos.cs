using Microsoft.EntityFrameworkCore;
using Servicios.Entidad.Tables;

namespace Servicios.Datos
{
    public class AccesoDatos : DbContext
    {
        public AccesoDatos(DbContextOptions<AccesoDatos> options) : base(options)
        {
            this.ChangeTracker.LazyLoadingEnabled = false;
        }

        public DbSet<Usuario> Usuario { get; set; }
    }
}
