using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace Servicios.Entidad.Model
{
    public class Inventario
    {
        [Key]
        public int InventarioId { get; set; }
        public string Nombre { get; set; }
        public DateTime FechaCompra { get; set; }
        public DateTime FechaVencimiento { get; set; }
        public byte Activo { get; set; }
        public decimal Cantidad { get; set; }
        public decimal Precio { get; set; }
        public int Porcentaje { get; set; }
        public string Proveedor { get; set; }
        public int MedidaId { get; set; }
        public virtual Medida Medida { get; set; }
    }
}
