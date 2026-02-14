"use client";

import { useEffect, useState } from "react";
import { fetchProperties, createProperty, deleteProperty } from "@/lib/api";
import { Property } from "@/types";

const ADMIN_TOKEN = "admin-secret-change-me";

function formatPrice(price: number) {
  if (price >= 10000000) return `${(price / 10000000).toFixed(1)} Cr`;
  if (price >= 100000) return `${(price / 100000).toFixed(1)} L`;
  return price.toLocaleString("en-IN");
}

const emptyForm = {
  title: "", description: "", property_type: "apartment", bhk: "",
  price: "", location: "", city: "", area_sqft: "", amenities: "", image_url: "",
};

export default function PropertiesPage() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(emptyForm);

  const load = () => fetchProperties().then(setProperties);
  useEffect(() => { load(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createProperty(ADMIN_TOKEN, {
      ...form,
      bhk: form.bhk ? parseInt(form.bhk) : null,
      price: parseFloat(form.price),
      area_sqft: form.area_sqft ? parseFloat(form.area_sqft) : null,
      amenities: form.amenities || null,
      image_url: form.image_url || null,
    });
    setForm(emptyForm);
    setShowForm(false);
    load();
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this property?")) return;
    await deleteProperty(ADMIN_TOKEN, id);
    load();
  };

  const inputClass = "bg-[#13110e] border border-[#2e2a24] rounded-sm px-4 py-2.5 text-sm font-sans text-[#f0ebe4] placeholder-[#3a342c] focus:outline-none focus:border-[#c8a97e]/50 transition-colors duration-300";

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-serif text-[#f0ebe4] tracking-tight">Properties</h1>
          <p className="text-[#5a4a3a] text-sm mt-1 font-sans">{properties.length} listings</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className={`px-5 py-2.5 rounded-sm text-sm font-sans font-medium transition-all duration-300 ${
            showForm
              ? "bg-[#1a1714] text-[#8a8279] border border-[#2e2a24] hover:text-[#f0ebe4]"
              : "bg-[#c8a97e] text-[#13110e] hover:bg-[#b8995e]"
          }`}
        >
          {showForm ? "Cancel" : "+ Add Property"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-[#1a1714] border border-[#2e2a24] rounded-sm p-6 mb-8 grid grid-cols-2 gap-4">
          <input className={inputClass} placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <select className={`${inputClass} appearance-none`} value={form.property_type} onChange={(e) => setForm({ ...form, property_type: e.target.value })}>
            <option value="apartment">Apartment</option>
            <option value="villa">Villa</option>
            <option value="plot">Plot</option>
            <option value="independent_house">Independent House</option>
          </select>
          <input className={inputClass} placeholder="Price (INR)" type="number" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} required />
          <input className={inputClass} placeholder="BHK" type="number" value={form.bhk} onChange={(e) => setForm({ ...form, bhk: e.target.value })} />
          <input className={inputClass} placeholder="Location" value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} required />
          <input className={inputClass} placeholder="City" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} required />
          <input className={inputClass} placeholder="Area (sqft)" type="number" value={form.area_sqft} onChange={(e) => setForm({ ...form, area_sqft: e.target.value })} />
          <input className={inputClass} placeholder='Amenities JSON e.g. ["parking","gym"]' value={form.amenities} onChange={(e) => setForm({ ...form, amenities: e.target.value })} />
          <textarea className={`${inputClass} col-span-2`} placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <button type="submit" className="col-span-2 bg-[#c8a97e] text-[#13110e] py-2.5 rounded-sm hover:bg-[#b8995e] font-sans font-medium text-sm tracking-wide transition-colors duration-300">Save Property</button>
        </form>
      )}

      <div className="bg-[#1a1714] border border-[#2e2a24] rounded-sm overflow-hidden">
        <table className="w-full text-sm font-sans">
          <thead className="border-b border-[#2e2a24] text-left">
            <tr>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">ID</th>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Title</th>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Type</th>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">BHK</th>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Price</th>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Location</th>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Status</th>
              <th className="px-5 py-3.5 text-[#5a4a3a] font-medium text-[10px] uppercase tracking-[0.15em]">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#2e2a24]/50">
            {properties.map((p) => (
              <tr key={p.id} className="hover:bg-[#f0ebe4]/2 transition-colors duration-300">
                <td className="px-5 py-3.5 text-[#5a4a3a]">#{p.id}</td>
                <td className="px-5 py-3.5 font-medium text-[#f0ebe4]">{p.title}</td>
                <td className="px-5 py-3.5 text-[#8a8279] capitalize">{p.property_type.replace("_", " ")}</td>
                <td className="px-5 py-3.5 text-[#8a8279]">{p.bhk ?? "-"}</td>
                <td className="px-5 py-3.5 text-[#c8a97e] font-medium">{formatPrice(p.price)}</td>
                <td className="px-5 py-3.5 text-[#8a8279]">{p.location}, {p.city}</td>
                <td className="px-5 py-3.5">
                  <span className={`text-[10px] uppercase tracking-[0.15em] px-2.5 py-1 rounded-sm font-sans ${
                    p.status === "available"
                      ? "bg-[#7a9e6e]/10 text-[#7a9e6e] border border-[#7a9e6e]/20"
                      : "bg-[#d4836a]/10 text-[#d4836a] border border-[#d4836a]/20"
                  }`}>
                    {p.status}
                  </span>
                </td>
                <td className="px-5 py-3.5">
                  <button onClick={() => handleDelete(p.id)} className="text-[#d4836a] hover:text-[#e09480] text-xs font-medium font-sans transition-colors duration-300">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
