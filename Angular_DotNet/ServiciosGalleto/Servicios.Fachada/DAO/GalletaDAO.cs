using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;
using Servicios.Datos;
using Servicios.Entidad.Model;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Servicios.Fachada.DAO
{
    public class GalletaDAO
    {
        public List<Galleta> GetAllGalleta(AccesoDatos DbContext)
        {
            return DbContext.Galleta.Include(p => p.Medida).ToList();
        }

        public int AgregarGalleta(AccesoDatos DbContext, Galleta data)
        {
            using (IDbContextTransaction transaction = DbContext.Database.BeginTransaction())
            {
                try
                {
                    DbContext.Galleta.Add(data);
                    DbContext.SaveChanges();

                    transaction.Commit();
                    return data.GalletaId;
                }
                catch (Exception ex)
                {
                    transaction.Rollback();
                    return 0;
                }
            }
        }

        public string ActualizarGalleta(AccesoDatos DbContext, Galleta data)
        {
            string mensaje = null;
            using (IDbContextTransaction transaction = DbContext.Database.BeginTransaction())
            {
                try
                {
                    DbContext.Galleta.Update(data);
                    DbContext.SaveChanges();

                    transaction.Commit();
                }
                catch (Exception ex)
                {
                    transaction.Rollback();
                    mensaje = "No se pudo actualizar la galleta.";
                }
            }
            return mensaje;
        }
    }
}
