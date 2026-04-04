# Proceso de Cierre Mensual - ADLG 11

## Qué hace este proceso
Registrar todos los movimientos del mes en `ADLG_ECTA.csv` y archivar los comprobantes en las carpetas correspondientes.

---

## Archivos de entrada
- `draft-credit/` → imágenes (.png/.jpg) de pagos de departamentos. El nombre del archivo ES el número de departamento (101, 202, etc.)
- `draft-debits/` → PDFs/imágenes de gastos. El nombre del archivo NO dice nada, hay que abrirlos.

---

## Paso 1 — Leer todos los archivos

### Créditos (draft-credit)
Abrir cada imagen para extraer:
- Monto
- Fecha del pago

### Débitos (draft-debits)
Abrir cada archivo para identificar:
- Tipo de gasto
- Monto
- Fecha
- Número de recibo (solo para Jardinería y Limpieza)

---

## Paso 2 — Iteraciones con el usuario

Antes de escribir el CSV, confirmar con el usuario:

1. **Montos ilegibles**: Si alguna boleta tiene montos tachados o poco claros, preguntar.
2. **Fechas ilegibles**: Si alguna fecha no se puede leer con certeza, preguntar.
3. **Archivos faltantes**: Revisar si falta el recibo de Seal (luz). Si no está en draft-debits, avisar.
4. **Cualquier otra duda**: Avisar antes de proceder.

---

## Paso 3 — Armar las entradas del CSV

### Formato de ordinal
`{mes}{año}{NNN}` → ej: `mar2026001`, `mar2026002`, ...

### Ordenar por fecha
Todos los movimientos del mes ordenados cronológicamente. Para el mismo día, seguir este orden (basado en meses anteriores):
1. Mantenimiento de Ascensor
2. Seal
3. Vigilancia
4. Créditos (pagos de departamentos)

### Formato de cada columna
```
Ordinal, Concept, Date, Reference, Debit, Credit
```
- **Date**: `D/MM/YY` (ej: `7/03/26`, `31/03/26`)
- **Reference**: Solo para Limpieza (`CLNSERV-XXX`), Jardinería (`GRDSERV-XXX`) y pagos de departamentos (`APTO101`, `APTO302`, etc.)
- **Debit**: Monto si es gasto, vacío si es ingreso
- **Credit**: Monto si es ingreso, vacío si es gasto

### Conceptos estándar
| Tipo | Concepto en CSV |
|------|----------------|
| Pago limpieza César Padilla | `Pago Cesar Padilla(Limpieza)` |
| Pago jardinería Leonardo Mendoza | `Pago Leonardo Mendoza(Jardinería)` |
| Ascensores S.A. | `Mantenimiento de Ascensor` |
| SEAL (luz) | `Seal` |
| Vigilancia | `Vigilancia` |
| Pago departamento | `Pago APTOXXX {MES}{AÑO}` ej: `Pago APTO302 MAR2026` |
| Otros gastos | Descripción corta según lo que dice la boleta |

---

## Paso 4 — Copiar archivos a destino

### ⚠️ IMPORTANTE: Siempre COPIAR (cp), nunca mover (mv)
Borrar los originales de draft solo después de que el usuario confirme que todo está bien.

### Créditos → `credits/{mes}{año}/`
Copiar los PNG/JPG con el mismo nombre de archivo.
- Ejemplo: `draft-credit/302.png` → `credits/mar2026/302.png`

### Débitos → `monthlyExpenses/{mes}{año}/`
Renombrar según tipo:
- **Jardinería y Limpieza** → usar número de recibo: `GRDSERV-014.pdf`, `CLNSERV-028.pdf`
- **Todos los demás** → usar ordinal del CSV: `mar2026011.pdf`, `mar2026013.jpg`, etc.

Si hay múltiples archivos para el mismo gasto (ej: boleta + comprobante de pago juntos en un PDF), usar el más completo.

### Crear carpetas si no existen
```
mkdir -p credits/{mes}{año}
mkdir -p monthlyExpenses/{mes}{año}
```

---

## Paso 5 — Verificar y confirmar

Después de copiar, mostrar al usuario:
1. Lista de entradas CSV agregadas (tabla)
2. Contenido de `credits/{mes}{año}/`
3. Contenido de `monthlyExpenses/{mes}{año}/`

Esperar confirmación antes de borrar los drafts.

---

## Paso 6 — Borrar drafts (solo tras confirmación)

```
rm draft-credit/*
rm draft-debits/*
```

---

## Notas importantes
- **APTO301 de marzo 2026**: Pagó el 1/04/26 (un día después del cierre de marzo). Se registra con la fecha real del pago.
- El CSV tiene un espacio al inicio en la última línea de feb2026 (` feb2026015`) — no corregir, es dato existente.
- Los archivos con nombre ordinal en monthlyExpenses pueden ser PDF o JPG según el original.
