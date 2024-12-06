using Servicios.Entidad.ViewModel;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace Servicios.Fachada.AppService
{
    public class InventarioAppService
    {
        public async Task<List<InventarioViewModel>> GetInventarioExterno()
        {
            List<InventarioViewModel> lista = new List<InventarioViewModel>();
            try
            {
                using (var httpClient = new HttpClient())
                {
                    HttpResponseMessage response = await httpClient.GetAsync("https://6720467ee7a5792f0530f68c.mockapi.io/api/v1/InventarioAppService");
                    response.EnsureSuccessStatusCode();
                    var jsonResponse = await response.Content.ReadAsStringAsync();
                    var listarespuesta = JsonSerializer.Deserialize<List<Dictionary<string, object>>>(jsonResponse);

                    foreach (var inventario in listarespuesta)
                    {
                        InventarioViewModel model = new InventarioViewModel();

                        model.id = int.Parse(inventario["id"].ToString());
                        model.nombre = inventario["nombre"].ToString();
                        model.fechaCompra = inventario["fechaCompra"].ToString();
                        model.fechaVencimiento = inventario["fechaVencimiento"].ToString();
                        model.activo = bool.Parse(inventario["activo"].ToString().ToLower()) ? 1 : 0;
                        model.cantidad = decimal.Parse(inventario["cantidad"].ToString());
                        model.precio = decimal.Parse(inventario["precio"].ToString());
                        model.porcentaje = int.Parse(inventario["porcentaje"].ToString());
                        model.proveedor = inventario["proveedor"].ToString();
                        model.idMedida = int.Parse(inventario["idMedida"].ToString());

                        lista.Add(model);
                    }
                }
            }
            catch (Exception ex)
            {
                lista = null;
            }
            return lista;
        }
    }
}
