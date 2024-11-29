using System;
using System.Collections.Generic;
using Servicios.Datos;
using Servicios.Entidad.Model;
using Servicios.Entidad.ViewModel;
using Servicios.Fachada.CQRS;

namespace Servicios.Fachada.AppService
{
    public class InventarioAppService
    {
        public List<InventarioViewModel> GetInventario(AccesoDatos DbContext, int estatus)
        {
            try
            {
                InventarioCQRS icqrs = new InventarioCQRS();

                List<Inventario> lista = icqrs.GetInventario(DbContext, estatus);
                List<InventarioViewModel> dataList = new List<InventarioViewModel>();

                foreach (Inventario i in lista)
                {
                    InventarioViewModel model = new InventarioViewModel();

                    model.id = i.InventarioId;
                    model.nombre = i.Nombre;
                    model.fechaCompra = i.FechaCompra.ToString();
                    model.fechaVencimiento = i.FechaVencimiento.ToString();
                    model.activo = i.Activo;
                    model.cantidad = i.Cantidad;
                    model.precio = i.Precio;
                    model.porcentaje = i.Porcentaje;
                    model.proveedor = i.Proveedor;
                    model.idMedida = i.MedidaId;
                    model.medida = i.Medida;

                    dataList.Add(model);
                }

                return dataList;
            }
            catch (Exception ex)
            {
                return null;
            }
        }

        public string AgregarInventario(AccesoDatos DbContext, List<InventarioViewModel> dataList)
        {
            try
            {
                InventarioCQRS icqrs = new InventarioCQRS();
                List<Inventario> inventarios = new List<Inventario>();
                foreach (InventarioViewModel i in dataList)
                {
                    Inventario inventario = new Inventario();

                    inventario.Nombre = i.nombre;
                    inventario.FechaCompra = DateTime.Parse(i.fechaCompra);
                    inventario.FechaVencimiento = DateTime.Parse(i.fechaVencimiento);
                    inventario.Activo = (byte)i.activo;
                    inventario.Cantidad = (decimal)i.cantidad;
                    inventario.Precio = (decimal)i.precio;
                    inventario.Porcentaje = (int)i.porcentaje;
                    inventario.Proveedor = i.proveedor;
                    inventario.MedidaId = i.idMedida;

                    inventarios.Add(inventario);
                }

                return icqrs.AgregarInventario(DbContext, inventarios);
            }
            catch (Exception ex)
            {
                return "Error al mapear los productos";
            }
        }

        public string ActualizarInventario(AccesoDatos DbContext, int id, InventarioViewModel data)
        {
            try
            {
                InventarioCQRS icqrs = new InventarioCQRS();
                Inventario inventario = new Inventario();

                inventario.Nombre = data.nombre;
                inventario.FechaCompra = DateTime.Parse(data.fechaCompra);
                inventario.FechaVencimiento = DateTime.Parse(data.fechaVencimiento);
                inventario.Activo = (byte)data.activo;
                inventario.Cantidad = (decimal)data.cantidad;
                inventario.Precio = (decimal)data.precio;
                inventario.Porcentaje = (int)data.porcentaje;
                inventario.Proveedor = data.proveedor;
                inventario.MedidaId = data.idMedida;

                return icqrs.ActualizarInventario(DbContext, id, inventario);
            }
            catch (Exception ex)
            {
                return "Error al mapear los productos";
            }
        }
    }
}
