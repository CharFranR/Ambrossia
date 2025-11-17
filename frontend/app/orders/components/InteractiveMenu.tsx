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
}

const fetchProducts = async (): Promise<Product[]> => {
  const res = await axios.get(
    `${process.env.NEXT_PUBLIC_API_ROOT || 'http://localhost:8000'}/products/`
  )
  return res.data
}

export default function InteractiveMenu({ onAdd }: { onAdd: (product: Product) => void }) {
  const { data: products, isLoading } = useQuery<Product[]>({
    queryKey: ['products'],
    queryFn: fetchProducts,
  })

  if (isLoading) return <div>Cargando productos...</div>

  return (
    <div className="p-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {products?.map((item: any) => (
        <motion.div
          key={item.id}
          whileHover={{ scale: 1.03 }}
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: item.id * 0.1, duration: 0.4 }}
        >
          <Card className="overflow-hidden rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300 bg-black">
            <CardHeader>
              <CardTitle className="text-lg font-semibold">{item.name}</CardTitle>
              <CardDescription>{item.description}</CardDescription>
            </CardHeader>
            <CardContent className="p-0 relative">
              <Image
                src={item.image}
                alt={item.name}
                className="aspect-video object-cover w-full h-56 rounded-b-2xl"
                width={500}
                height={500}
              />
              <div className="absolute bottom-3 right-3">
                <Button
                  variant="default"
                  size="sm"
                  className="flex items-center gap-1 bg-white-600 hover:bg-white-700"
                  onClick={() => onAdd(item)}
                >
                  <PlusCircle className="h-4 w-4" /> Add
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}
