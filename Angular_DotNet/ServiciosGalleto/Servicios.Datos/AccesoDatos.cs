using Microsoft.EntityFrameworkCore;
using Servicios.Entidad.Model;
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
        public DbSet<Medida> Medida { get; set; }
        public DbSet<Inventario> Inventario { get; set; }
        public DbSet<Galleta> Galleta { get; set; }
        public DbSet<Receta> Receta { get; set; }
    }
}
