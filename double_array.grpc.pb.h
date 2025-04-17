// Generated by the gRPC C++ plugin.
// If you make any local change, they will be lost.
// source: double_array.proto
#ifndef GRPC_double_5farray_2eproto__INCLUDED
#define GRPC_double_5farray_2eproto__INCLUDED

#include "double_array.pb.h"

#include <functional>
#include <grpcpp/generic/async_generic_service.h>
#include <grpcpp/support/async_stream.h>
#include <grpcpp/support/async_unary_call.h>
#include <grpcpp/support/client_callback.h>
#include <grpcpp/client_context.h>
#include <grpcpp/completion_queue.h>
#include <grpcpp/support/message_allocator.h>
#include <grpcpp/support/method_handler.h>
#include <grpcpp/impl/proto_utils.h>
#include <grpcpp/impl/rpc_method.h>
#include <grpcpp/support/server_callback.h>
#include <grpcpp/impl/server_callback_handlers.h>
#include <grpcpp/server_context.h>
#include <grpcpp/impl/service_type.h>
#include <grpcpp/support/status.h>
#include <grpcpp/support/stub_options.h>
#include <grpcpp/support/sync_stream.h>
#include <grpcpp/ports_def.inc>

namespace doublearrayservice {

// Service definition
class DoubleArrayService final {
 public:
  static constexpr char const* service_full_name() {
    return "doublearrayservice.DoubleArrayService";
  }
  class StubInterface {
   public:
    virtual ~StubInterface() {}
    // RPC method to send an array of doubles and receive a count
    virtual ::grpc::Status SendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::doublearrayservice::CountResponse* response) = 0;
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::doublearrayservice::CountResponse>> AsyncSendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::doublearrayservice::CountResponse>>(AsyncSendDoubleArrayRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::doublearrayservice::CountResponse>> PrepareAsyncSendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReaderInterface< ::doublearrayservice::CountResponse>>(PrepareAsyncSendDoubleArrayRaw(context, request, cq));
    }
    class async_interface {
     public:
      virtual ~async_interface() {}
      // RPC method to send an array of doubles and receive a count
      virtual void SendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest* request, ::doublearrayservice::CountResponse* response, std::function<void(::grpc::Status)>) = 0;
      virtual void SendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest* request, ::doublearrayservice::CountResponse* response, ::grpc::ClientUnaryReactor* reactor) = 0;
    };
    typedef class async_interface experimental_async_interface;
    virtual class async_interface* async() { return nullptr; }
    class async_interface* experimental_async() { return async(); }
   private:
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::doublearrayservice::CountResponse>* AsyncSendDoubleArrayRaw(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) = 0;
    virtual ::grpc::ClientAsyncResponseReaderInterface< ::doublearrayservice::CountResponse>* PrepareAsyncSendDoubleArrayRaw(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) = 0;
  };
  class Stub final : public StubInterface {
   public:
    Stub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());
    ::grpc::Status SendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::doublearrayservice::CountResponse* response) override;
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::doublearrayservice::CountResponse>> AsyncSendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::doublearrayservice::CountResponse>>(AsyncSendDoubleArrayRaw(context, request, cq));
    }
    std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::doublearrayservice::CountResponse>> PrepareAsyncSendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) {
      return std::unique_ptr< ::grpc::ClientAsyncResponseReader< ::doublearrayservice::CountResponse>>(PrepareAsyncSendDoubleArrayRaw(context, request, cq));
    }
    class async final :
      public StubInterface::async_interface {
     public:
      void SendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest* request, ::doublearrayservice::CountResponse* response, std::function<void(::grpc::Status)>) override;
      void SendDoubleArray(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest* request, ::doublearrayservice::CountResponse* response, ::grpc::ClientUnaryReactor* reactor) override;
     private:
      friend class Stub;
      explicit async(Stub* stub): stub_(stub) { }
      Stub* stub() { return stub_; }
      Stub* stub_;
    };
    class async* async() override { return &async_stub_; }

   private:
    std::shared_ptr< ::grpc::ChannelInterface> channel_;
    class async async_stub_{this};
    ::grpc::ClientAsyncResponseReader< ::doublearrayservice::CountResponse>* AsyncSendDoubleArrayRaw(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) override;
    ::grpc::ClientAsyncResponseReader< ::doublearrayservice::CountResponse>* PrepareAsyncSendDoubleArrayRaw(::grpc::ClientContext* context, const ::doublearrayservice::DoubleArrayRequest& request, ::grpc::CompletionQueue* cq) override;
    const ::grpc::internal::RpcMethod rpcmethod_SendDoubleArray_;
  };
  static std::unique_ptr<Stub> NewStub(const std::shared_ptr< ::grpc::ChannelInterface>& channel, const ::grpc::StubOptions& options = ::grpc::StubOptions());

  class Service : public ::grpc::Service {
   public:
    Service();
    virtual ~Service();
    // RPC method to send an array of doubles and receive a count
    virtual ::grpc::Status SendDoubleArray(::grpc::ServerContext* context, const ::doublearrayservice::DoubleArrayRequest* request, ::doublearrayservice::CountResponse* response);
  };
  template <class BaseClass>
  class WithAsyncMethod_SendDoubleArray : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithAsyncMethod_SendDoubleArray() {
      ::grpc::Service::MarkMethodAsync(0);
    }
    ~WithAsyncMethod_SendDoubleArray() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SendDoubleArray(::grpc::ServerContext* /*context*/, const ::doublearrayservice::DoubleArrayRequest* /*request*/, ::doublearrayservice::CountResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestSendDoubleArray(::grpc::ServerContext* context, ::doublearrayservice::DoubleArrayRequest* request, ::grpc::ServerAsyncResponseWriter< ::doublearrayservice::CountResponse>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  typedef WithAsyncMethod_SendDoubleArray<Service > AsyncService;
  template <class BaseClass>
  class WithCallbackMethod_SendDoubleArray : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithCallbackMethod_SendDoubleArray() {
      ::grpc::Service::MarkMethodCallback(0,
          new ::grpc::internal::CallbackUnaryHandler< ::doublearrayservice::DoubleArrayRequest, ::doublearrayservice::CountResponse>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::doublearrayservice::DoubleArrayRequest* request, ::doublearrayservice::CountResponse* response) { return this->SendDoubleArray(context, request, response); }));}
    void SetMessageAllocatorFor_SendDoubleArray(
        ::grpc::MessageAllocator< ::doublearrayservice::DoubleArrayRequest, ::doublearrayservice::CountResponse>* allocator) {
      ::grpc::internal::MethodHandler* const handler = ::grpc::Service::GetHandler(0);
      static_cast<::grpc::internal::CallbackUnaryHandler< ::doublearrayservice::DoubleArrayRequest, ::doublearrayservice::CountResponse>*>(handler)
              ->SetMessageAllocator(allocator);
    }
    ~WithCallbackMethod_SendDoubleArray() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SendDoubleArray(::grpc::ServerContext* /*context*/, const ::doublearrayservice::DoubleArrayRequest* /*request*/, ::doublearrayservice::CountResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* SendDoubleArray(
      ::grpc::CallbackServerContext* /*context*/, const ::doublearrayservice::DoubleArrayRequest* /*request*/, ::doublearrayservice::CountResponse* /*response*/)  { return nullptr; }
  };
  typedef WithCallbackMethod_SendDoubleArray<Service > CallbackService;
  typedef CallbackService ExperimentalCallbackService;
  template <class BaseClass>
  class WithGenericMethod_SendDoubleArray : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithGenericMethod_SendDoubleArray() {
      ::grpc::Service::MarkMethodGeneric(0);
    }
    ~WithGenericMethod_SendDoubleArray() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SendDoubleArray(::grpc::ServerContext* /*context*/, const ::doublearrayservice::DoubleArrayRequest* /*request*/, ::doublearrayservice::CountResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
  };
  template <class BaseClass>
  class WithRawMethod_SendDoubleArray : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawMethod_SendDoubleArray() {
      ::grpc::Service::MarkMethodRaw(0);
    }
    ~WithRawMethod_SendDoubleArray() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SendDoubleArray(::grpc::ServerContext* /*context*/, const ::doublearrayservice::DoubleArrayRequest* /*request*/, ::doublearrayservice::CountResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    void RequestSendDoubleArray(::grpc::ServerContext* context, ::grpc::ByteBuffer* request, ::grpc::ServerAsyncResponseWriter< ::grpc::ByteBuffer>* response, ::grpc::CompletionQueue* new_call_cq, ::grpc::ServerCompletionQueue* notification_cq, void *tag) {
      ::grpc::Service::RequestAsyncUnary(0, context, request, response, new_call_cq, notification_cq, tag);
    }
  };
  template <class BaseClass>
  class WithRawCallbackMethod_SendDoubleArray : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithRawCallbackMethod_SendDoubleArray() {
      ::grpc::Service::MarkMethodRawCallback(0,
          new ::grpc::internal::CallbackUnaryHandler< ::grpc::ByteBuffer, ::grpc::ByteBuffer>(
            [this](
                   ::grpc::CallbackServerContext* context, const ::grpc::ByteBuffer* request, ::grpc::ByteBuffer* response) { return this->SendDoubleArray(context, request, response); }));
    }
    ~WithRawCallbackMethod_SendDoubleArray() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable synchronous version of this method
    ::grpc::Status SendDoubleArray(::grpc::ServerContext* /*context*/, const ::doublearrayservice::DoubleArrayRequest* /*request*/, ::doublearrayservice::CountResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    virtual ::grpc::ServerUnaryReactor* SendDoubleArray(
      ::grpc::CallbackServerContext* /*context*/, const ::grpc::ByteBuffer* /*request*/, ::grpc::ByteBuffer* /*response*/)  { return nullptr; }
  };
  template <class BaseClass>
  class WithStreamedUnaryMethod_SendDoubleArray : public BaseClass {
   private:
    void BaseClassMustBeDerivedFromService(const Service* /*service*/) {}
   public:
    WithStreamedUnaryMethod_SendDoubleArray() {
      ::grpc::Service::MarkMethodStreamed(0,
        new ::grpc::internal::StreamedUnaryHandler<
          ::doublearrayservice::DoubleArrayRequest, ::doublearrayservice::CountResponse>(
            [this](::grpc::ServerContext* context,
                   ::grpc::ServerUnaryStreamer<
                     ::doublearrayservice::DoubleArrayRequest, ::doublearrayservice::CountResponse>* streamer) {
                       return this->StreamedSendDoubleArray(context,
                         streamer);
                  }));
    }
    ~WithStreamedUnaryMethod_SendDoubleArray() override {
      BaseClassMustBeDerivedFromService(this);
    }
    // disable regular version of this method
    ::grpc::Status SendDoubleArray(::grpc::ServerContext* /*context*/, const ::doublearrayservice::DoubleArrayRequest* /*request*/, ::doublearrayservice::CountResponse* /*response*/) override {
      abort();
      return ::grpc::Status(::grpc::StatusCode::UNIMPLEMENTED, "");
    }
    // replace default version of method with streamed unary
    virtual ::grpc::Status StreamedSendDoubleArray(::grpc::ServerContext* context, ::grpc::ServerUnaryStreamer< ::doublearrayservice::DoubleArrayRequest,::doublearrayservice::CountResponse>* server_unary_streamer) = 0;
  };
  typedef WithStreamedUnaryMethod_SendDoubleArray<Service > StreamedUnaryService;
  typedef Service SplitStreamedService;
  typedef WithStreamedUnaryMethod_SendDoubleArray<Service > StreamedService;
};

}  // namespace doublearrayservice


#include <grpcpp/ports_undef.inc>
#endif  // GRPC_double_5farray_2eproto__INCLUDED
