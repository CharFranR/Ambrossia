'use client'

import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardDescription, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { PlusCircle } from 'lucide-react'
import Image from 'next/image'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

type Product = {
  id: number
  name: string
  description?: string
  price: number
  image?: string
  category?: string
}

const fetchProducts = async (): Promise<Product[]> => {
  const res = await axios.get(
    `${process.env.NEXT_PUBLIC_API_ROOT || 'http://localhost:8000'}/products/`
  )
  return res.data
}

export default function InteractiveMenu({
  onAdd,
  category,
}: {
  onAdd: (product: Product) => void
  category?: string
}) {
  const { data: products, isLoading } = useQuery<Product[]>({
    queryKey: ['products'],
    queryFn: fetchProducts,
  })

  const filtered = category && category !== "all"
    ? products?.filter((p: Product) => p.category === category)
    : products

  if (isLoading)
    return (
      <div className="text-center py-6 text-gray-500">
        Cargando productos...
      </div>
    )

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {filtered?.map((item: Product) => (
        <motion.div
          key={item.id}
          whileHover={{ scale: 1.03 }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <Card className="overflow-hidden rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 bg-background text-foreground">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">{item.name}</CardTitle>
              <CardDescription>{item.description}</CardDescription>
            </CardHeader>
            <CardContent className="relative p-0">
              {item.image && (
                <Image
                  src={item.image}
                  alt={item.name}
                  className="aspect-video object-cover w-full h-56 rounded-b-2xl"
                  width={500}
                  height={500}
                />
              )}
              <div className="absolute bottom-3 right-3">
                <Button
                  variant="default"
                  size="sm"
                  className="flex items-center gap-1"
                  onClick={() => onAdd(item)}
                >
                  <PlusCircle className="h-4 w-4" /> Agregar
                </Button>
              </div>
              <div className="absolute bottom-3 left-3 font-bold text-sky-700 bg-white/80 px-2 py-1 rounded">
                ${item.price?.toFixed(2)}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
