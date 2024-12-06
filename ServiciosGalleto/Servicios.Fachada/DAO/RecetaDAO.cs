using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;
using Servicios.Datos;
using Servicios.Entidad.Model;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Servicios.Fachada.DAO
{
    public class RecetaDAO
    {
        public List<Receta> GetReceta(AccesoDatos DbContext, int GalletaId)
        {
            return DbContext.Receta.Include(p => p.Galleta).Include(p => p.Inventario).Include(p => p.Medida).Where(p => p.GalletaId == GalletaId).ToList();
        }

        public string AgregarReceta(AccesoDatos DbContext, int GalletaId, List<Receta> dataList)
        {
            string mensaje = null;
            using (IDbContextTransaction transaction = DbContext.Database.BeginTransaction())
            {
                try
                {
                    List<Receta> recetaActual = DbContext.Receta.Where(p => p.GalletaId == GalletaId).ToList();
                    foreach (Receta receta in recetaActual)
                    {
                        DbContext.Receta.Remove(receta);
                        DbContext.SaveChanges();
                    }

                    foreach (Receta receta in dataList)
                    {
                        DbContext.Receta.Add(receta);
                        DbContext.SaveChanges();
                    }

                    transaction.Commit();
                    mensaje = null;
                }
                catch (Exception ex)
                {
                    transaction.Rollback();
                    mensaje = "No se pudo guardar la lista en el dao por problemas con el producto: " + mensaje;
                }
            }
            return mensaje;
        }
    }
}
