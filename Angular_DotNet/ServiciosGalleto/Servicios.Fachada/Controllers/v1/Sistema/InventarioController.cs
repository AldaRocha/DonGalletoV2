using Microsoft.AspNetCore.Mvc;
using Security;
using Servicios.Datos;
using Servicios.Entidad.Model;
using Servicios.Entidad.ViewModel;
using Servicios.Fachada.AppService;
using Servicios.Fachada.CQRS;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Servicios.Fachada.Controllers.v1.Sistema
{
    [Route("api/v1/almacen")]
    public class InventarioController : ControllerBase
    {
        AccesoDatos DbContext;
        Response response;

        public InventarioController(AccesoDatos DbContext)
        {
            this.DbContext = DbContext;
            this.response = new Response();
        }

        [HttpGet("{Activo}")]
        public async Task<ActionResult<Response>> GetAlmacen(int activo)
        {
            try
            {
                InventarioAppService ias = new InventarioAppService();
                InventarioCQRS icqrs = new InventarioCQRS();

                List<Inventario> lista = icqrs.GetInventario(DbContext, activo);
                //List<InventarioViewModel> externo = await ias.GetInventarioExterno();
                List<InventarioViewModel> dataList = new List<InventarioViewModel>();

                foreach (Inventario i in lista)
                {
                    InventarioViewModel model = new InventarioViewModel();
                    MedidaViewModel modelMedida = new MedidaViewModel();

                    modelMedida.id = i.Medida.MedidaId;
                    modelMedida.nombre = i.Medida.Nombre;

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
                    model.medida = modelMedida;

                    dataList.Add(model);
                }

                //foreach (InventarioViewModel inventario in externo)
                //{
                  //  dataList.Add(inventario);
                //}

                return response.Ok("", dataList);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpPost]
        public ActionResult<Response> AgregarAlmacen([FromBody] RequestInterface request)
        {
            try
            {
                List<InventarioViewModel> dataList = request.getData<List<InventarioViewModel>>();
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

                string mensaje = icqrs.AgregarInventario(DbContext, inventarios);

                return response.Ok(mensaje);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpPut]
        public ActionResult<Response> ActualizarAlmacen([FromBody] RequestInterface request)
        {
            try
            {
                InventarioViewModel data = request.getData<InventarioViewModel>();
                InventarioCQRS icqrs = new InventarioCQRS();
                Inventario inventario = new Inventario();

                inventario.InventarioId = (int)data.id;
                inventario.Nombre = data.nombre;
                inventario.FechaCompra = DateTime.Parse(data.fechaCompra);
                inventario.FechaVencimiento = DateTime.Parse(data.fechaVencimiento);
                inventario.Activo = (byte)data.activo;
                inventario.Cantidad = (decimal)data.cantidad;
                inventario.Precio = (decimal)data.precio;
                inventario.Porcentaje = (int)data.porcentaje;
                inventario.Proveedor = data.proveedor;
                inventario.MedidaId = data.idMedida;

                string mensaje = icqrs.ActualizarInventario(DbContext, inventario);

                return response.Ok(mensaje);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }

        [HttpDelete("{id}")]
        public ActionResult<Response> DesactivarAlmacen(int id)
        {
            try
            {
                InventarioCQRS icqrs = new InventarioCQRS();

                string mensaje = icqrs.DesactivarInventario(DbContext, id);

                return response.Ok(mensaje);
            }
            catch (Exception ex)
            {
                return new ObjectResult(new { message = ex.Message });
            }
        }
    }
}
