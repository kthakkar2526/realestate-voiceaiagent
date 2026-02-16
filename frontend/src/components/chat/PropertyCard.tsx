"use client";

import { Property } from "@/types";

function formatPrice(price: number) {
  if (price >= 10000000) return `${(price / 10000000).toFixed(1)} Cr`;
  if (price >= 100000) return `${(price / 100000).toFixed(1)} L`;
  return price.toLocaleString("en-IN");
}

export default function PropertyCard({ property }: { property: Property }) {
  const amenities = property.amenities ? JSON.parse(property.amenities) : [];

  return (
    <div className="bg-white border border-[#e0d9cf] rounded-sm p-4 my-2 hover:border-[#c8a97e]/50 transition-colors duration-500">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="font-serif text-[#1a1714] tracking-tight">{property.title}</h3>
          <p className="text-xs text-[#8a8279] font-sans mt-0.5">
            {property.location}, {property.city}
          </p>
        </div>
        <span className="text-base font-serif text-[#a88b5e]">
          ₹{formatPrice(property.price)}
        </span>
      </div>
      {property.description && (
        <p className="text-xs text-[#8a8279] mt-2.5 leading-relaxed font-sans">{property.description}</p>
      )}
      <div className="flex gap-2 mt-3 text-xs font-sans">
        {property.bhk && <span className="bg-[#f3efe9] border border-[#e0d9cf] text-[#5a4a3a] px-2.5 py-1 rounded-sm">{property.bhk} BHK</span>}
        <span className="bg-[#f3efe9] border border-[#e0d9cf] text-[#5a4a3a] px-2.5 py-1 rounded-sm capitalize">{property.property_type.replace("_", " ")}</span>
        {property.area_sqft && <span className="bg-[#f3efe9] border border-[#e0d9cf] text-[#5a4a3a] px-2.5 py-1 rounded-sm">{property.area_sqft} sqft</span>}
      </div>
      {amenities.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-2.5">
          {amenities.map((a: string) => (
            <span key={a} className="text-[10px] bg-[#c8a97e]/10 text-[#a88b5e] px-2 py-0.5 rounded-sm border border-[#c8a97e]/20 capitalize font-sans">
              {a}
            </span>
          ))}
        </div>
      )}
      <p className="text-[10px] text-[#b0a89e] mt-2.5 font-sans tracking-wide">Property #{property.id}</p>
    </div>
  );
}
