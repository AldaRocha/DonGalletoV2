using Servicios.Datos;
using Servicios.Entidad.Model;
using Servicios.Fachada.DAO;
using System;
using System.Collections.Generic;

namespace Servicios.Fachada.CQRS
{
    public class InventarioCQRS
    {
        public List<Inventario> GetInventario(AccesoDatos DbContext, int estatus)
        {
            try
            {
                List<Inventario> dataList = new List<Inventario>();
                InventarioDAO idao = new InventarioDAO();

                if (estatus == -1)
                {
                    dataList = idao.GetAllInventario(DbContext);
                }
                else
                {
                    dataList = idao.GetAllInventarioEstatus(DbContext, estatus);
                }

                return dataList;
            }
            catch (Exception ex)
            {
                return null;
            }
        }

        public string AgregarInventario(AccesoDatos DbContext, List<Inventario> dataList)
        {
            string mensaje = null;
            try
            {
                bool guardar = true;

                foreach (Inventario inventario in dataList)
                {
                    mensaje = inventario.Nombre;

                    if (inventario.Nombre == null || inventario.Nombre == "")
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.FechaCompra == null)
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.FechaVencimiento == null)
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.Activo == null)
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.Cantidad == null || inventario.Cantidad == 0)
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.Precio == null || inventario.Precio == 0)
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.Porcentaje == null || inventario.Porcentaje == 0)
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.Proveedor == null || inventario.Proveedor == "")
                    {
                        guardar = false;
                        break;
                    }

                    if (inventario.MedidaId == null || inventario.MedidaId == 0)
                    {
                        guardar = false;
                        break;
                    }
                }

                if (guardar)
                {
                    InventarioDAO idao = new InventarioDAO();

                    mensaje = idao.AgregarInventario(DbContext, dataList);
                }
                else
                {
                    mensaje = "Al menos un dato del producto '" + mensaje + "' esta vacio";
                }
            }
            catch (Exception ex)
            {
                mensaje = "No se pudo validar la lista en el cqrs por problemas con el producto: " + mensaje;
            }
            return mensaje;
        }

        public string ActualizarInventario(AccesoDatos DbContext, Inventario data)
        {
            string mensaje = null;
            try
            {
                bool guardar = true;

                mensaje = data.Nombre;

                if (data.Nombre == null || data.Nombre == "")
                {
                    guardar = false;
                }

                if (data.FechaCompra == null)
                {
                    guardar = false;
                }

                if (data.FechaVencimiento == null)
                {
                    guardar = false;
                }

                if (data.Activo == null)
                {
                    guardar = false;
                }

                if (data.Cantidad == null || data.Cantidad == 0)
                {
                    guardar = false;
                }

                if (data.Precio == null || data.Precio == 0)
                {
                    guardar = false;
                }

                if (data.Porcentaje == null || data.Porcentaje == 0)
                {
                    guardar = false;
                }

                if (data.Proveedor == null || data.Proveedor == "")
                {
                    guardar = false;
                }

                if (data.MedidaId == null || data.MedidaId == 0)
                {
                    guardar = false;
                }

                if (guardar)
                {
                    InventarioDAO idao = new InventarioDAO();

                    mensaje = idao.ActualizarInventario(DbContext, data);
                }
                else
                {
                    mensaje = "Al menos un dato del producto '" + mensaje + "' esta vacio";
                }
            }
            catch (Exception ex)
            {
                mensaje = "No se pudo validar la lista en el cqrs por problemas con el producto: " + mensaje;
            }
            return mensaje;
        }

        public string DesactivarInventario(AccesoDatos DbContext, int id)
        {
            try
            {
                if (id == null || id == 0)
                {
                    return "El id esta vacío";
                }
                else
                {
                    InventarioDAO idao = new InventarioDAO();

                    return idao.DesactivarInventario(DbContext, id);
                }
            }
            catch (Exception ex)
            {
                return "Error al validar el id en el cqrs";
            }
        }
    }
}
