using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Storage;
using Servicios.Datos;
using Servicios.Entidad.Model;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Servicios.Fachada.DAO
{
    public class InventarioDAO
    {
        public List<Inventario> GetAllInventario(AccesoDatos DbContext)
        {
            return DbContext.Inventario.Include(p => p.Medida).ToList();
        }

        public List<Inventario> GetAllInventarioEstatus(AccesoDatos DbContext, int estatus)
        {
            return DbContext.Inventario.Include(p => p.Medida).Where(p => p.Activo == estatus).ToList();
        }

        public string AgregarInventario(AccesoDatos DbContext, List<Inventario> dataList)
        {
            string mensaje = null;
            using (IDbContextTransaction transaction = DbContext.Database.BeginTransaction())
            {
                try
                {
                    foreach (Inventario inventario in dataList)
                    {
                        mensaje = inventario.Nombre;

                        DbContext.Inventario.Add(inventario);
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

        public string ActualizarInventario(AccesoDatos DbContext, int id, Inventario data)
        {
            string mensaje = null;
            using (IDbContextTransaction transaction = DbContext.Database.BeginTransaction())
            {
                try
                {
                    Inventario inventario = DbContext.Inventario.Where(p => p.InventarioId == id).FirstOrDefault();
                    if (inventario == null)
                    {
                        mensaje = "Producto no encontrado.";
                    }
                    else
                    {
                        DbContext.Inventario.Update(data);
                        DbContext.SaveChanges();

                        transaction.Commit();
                    }

                }
                catch (Exception ex)
                {
                    transaction.Rollback();
                    mensaje = "No se pudo actualizar la lista por problemas con el producto: " + mensaje;
                }
            }
            return mensaje;
        }

        public string DesactivarInventario(AccesoDatos DbContext, int id)
        {
            using (IDbContextTransaction transaction = DbContext.Database.BeginTransaction())
            {
                try
                {
                    Inventario inventario = DbContext.Inventario.Where(p => p.InventarioId == id).FirstOrDefault();
                    if (inventario == null)
                    {
                        return "Producto no encontrado";
                    }

                    inventario.Activo = 0;

                    DbContext.Update(inventario);
                    DbContext.SaveChanges();

                    transaction.Commit();
                    return "Producto desactivado con exito.";
                }
                catch (Exception ex)
                {
                    transaction.Rollback();
                    return "Error al eliminar el producto: " + ex.Message;
                }
            }
        }
    }
}
