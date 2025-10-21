import { AppSidebar } from "@/components/app-sidebar";

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";

import {
  InputGroup,
  InputGroupAddon,
  InputGroupButton,
  InputGroupInput,
} from "@/components/ui/input-group";

import { Separator } from "@/components/ui/separator";

import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";

export default function HomePage() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-12">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator
              orientation="vertical"
              className="mr-2 data-[orientation=vertical]:h-4"
            />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem className="hidden md:block">
                  <BreadcrumbLink href="#">
                    Building Your Application
                  </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator className="hidden md:block" />
                <BreadcrumbItem>
                  <BreadcrumbPage>Data Fetching</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        </header>

        {/* Contenedor principal que ocupa el espacio restante después del header */}
        <div className="flex flex-col" style={{ height: "calc(100vh - 4rem)" }}>
          {/* Área de mensajes scrollable - ocupa todo el espacio disponible */}
          <div className="flex-1 overflow-auto p-4">
            <div className="max-w-2xl mx-auto w-full">
              <div className="flex flex-col gap-4">
                {/* Mensaje recibido */}
                <div className="flex justify-start">
                  <div className="bg-muted rounded-xl px-3 py-2 max-w-[80%]">
                    <p className="text-sm">Quiero buscar algo</p>
                  </div>
                </div>

                {/* Mensaje enviado */}
                <div className="flex justify-end">
                  <div className="bg-primary text-primary-foreground rounded-xl px-3 py-2 max-w-[80%]">
                    <p className="text-sm">¡Claro! ¿Qué te gustaría buscar?</p>
                  </div>
                </div>

                {/* Agrega más mensajes aquí para probar el scroll */}
                <div className="flex justify-start">
                  <div className="bg-muted rounded-xl px-3 py-2 max-w-[80%]">
                    <p className="text-sm">Otro mensaje recibido</p>
                  </div>
                </div>

                <div className="flex justify-end">
                  <div className="bg-primary text-primary-foreground rounded-xl px-3 py-2 max-w-[80%]">
                    <p className="text-sm">Respuesta del usuario</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Área de input fija en la parte inferior */}
          <div className="border-t p-4 bg-background">
            <div className="max-w-2xl mx-auto w-full">
              <InputGroup className="w-full">
                <InputGroupInput
                  placeholder="Escribe tu mensaje..."
                  className="flex-1"
                />
                <InputGroupAddon align="inline-end">
                  <InputGroupButton variant="secondary">
                    Enviar
                  </InputGroupButton>
                </InputGroupAddon>
              </InputGroup>
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
